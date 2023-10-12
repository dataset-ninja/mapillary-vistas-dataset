# https://www.mapillary.com/dataset/vistas

import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from supervisely.io.json import load_json_file
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "Mapillary Vistas Dataset"
    dataset_path = "/mnt/d/datasetninja-raw/mapillary-vistas-dataset"
    batch_size = 1
    classes_json_path = "/mnt/d/datasetninja-raw/mapillary-vistas-dataset/config_v2.0.json"
    images_folder = "images"
    masks_folder = "v2.0/labels"
    images_ext = ".jpg"
    masks_ext = ".png"
    poly_masks_ext = ".json"
    poly_masks_folder = "v2.0/polygons"

    def create_ann(image_path):
        labels = []

        mask_name = get_file_name_with_ext(image_path).replace(images_ext, poly_masks_ext)
        mask_path = os.path.join(masks_path, mask_name)
        if file_exists(mask_path):
            data = load_json_file(mask_path)
            img_height = data["height"]
            img_wight = data["width"]
            for curr_ann_data in data["objects"]:
                class_name = name_to_readable[curr_ann_data["label"]]
                obj_class = meta.get_obj_class(class_name)
                exterior = []
                coords = curr_ann_data["polygon"]
                for curr_coord in coords:
                    exterior.append([int(curr_coord[1]), int(curr_coord[0])])
                if len(exterior) < 3:
                    continue
                poligon = sly.Polygon(exterior)

                root_macro_classes = curr_ann_data["label"].split("--")[:-1]

                label_tags = [
                    sly.Tag(tag_meta)
                    for tag_meta in tag_metas
                    if tag_meta.name in root_macro_classes
                ]

                label_poly = sly.Label(poligon, obj_class, tags=label_tags)
                labels.append(label_poly)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta()

    classes_data = load_json_file(classes_json_path)["labels"]
    name_to_readable = {}

    for curr_class in classes_data:
        obj_class = sly.ObjClass(
            curr_class["readable"].lower(), sly.Polygon, color=curr_class["color"]
        )
        name_to_readable[curr_class["name"]] = obj_class.name
        meta = meta.add_obj_class(obj_class)

        tag_names = curr_class["name"].split("--")[:-1]

        for tag_name in tag_names:
            if tag_name not in meta.tag_metas.keys():
                meta = meta.add_tag_metas([sly.TagMeta(tag_name, sly.TagValueType.NONE)])

    api.project.update_meta(project.id, meta.to_json())
    tag_metas = meta.tag_metas.items()

    for ds_name in ["training", "validation", "testing"]:
        ds_path = os.path.join(dataset_path, ds_name)
        if dir_exists(ds_path):
            dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

            images_path = os.path.join(ds_path, images_folder)
            masks_path = os.path.join(ds_path, poly_masks_folder)

            images_names = os.listdir(images_path)

            progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

            for img_names_batch in sly.batched(images_names, batch_size=batch_size):
                img_pathes_batch = [
                    os.path.join(images_path, im_name) for im_name in img_names_batch
                ]

                img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
                img_ids = [im_info.id for im_info in img_infos]

                if ds_name != "testing":
                    anns = [create_ann(image_path) for image_path in img_pathes_batch]
                    api.annotation.upload_anns(img_ids, anns)

                progress.iters_done_report(len(img_names_batch))
    return project
