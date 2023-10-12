The **Mapillary Vistas Dataset v2.0** is a substantial, street-level image dataset containing 25,000 high-resolution images annotated across 124 classes (70 instance-specific, 46 stuff, 8 void or crowd). Annotation adopts a dense, fine-grained style using polygons to delineate individual objects. The dataset, authored by the dataset creators, is notably larger, by a factor of 5, than the combined fine annotations in Cityscapes. It encompasses images captured worldwide, encompassing diverse weather, seasonal, and daytime conditions. The images are sourced from various devices such as mobile phones, tablets, action cameras, professional capturing rigs, and different experienced photographers, thus embracing diversity, detail richness, and global coverage.

The default benchmark tasks defined by the authors are semantic image segmentation and instance-specific image segmentation, with the intent of advancing state-of-the-art methods for understanding road scenes visually. The dataset is built upon images extracted from [www.mapillary.com](www.mapillary.com), a community-led platform for visualizing the world through street-level photos. Anyone can contribute photos of various places, and the data is available under a CC-BY-SA license agreement.

<img src="https://github.com/dataset-ninja/surgical-scene-segmentation-in-robotic-gastrectomy/assets/78355358/8529f9f1-0fc8-4bd4-8a3e-27a6d7e9d6d0" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Illustration of number of labeled instances per category and corresponding macro- and root-level class (v1.2)</span>

## Image and Category Selection

In order to accept an image for the semantic annotation process, several criteria have to be met. First, the image resolution has to be at least full HD, i.e., a minimum width/height of 1920x1080 was imposed. Additionally, approximately 90% of the images should be selected from road/sidewalk views in urban areas, and the remaining ones from highways, rural areas, and off-road. The database was queried in a way to randomly present potential candidates to a human for further evaluation and selection. Images with strong wide-angle views or 360° images were removed. Degraded images exhibiting strong motion blur, rolling shutter artifacts, interlacing artifacts, major windshield reflections, or containing dominant image parts from the capturing vehicle/device were removed as well. A small amount of distortion for motion blur was accepted, as long as individual objects could still be recognized and precisely annotated.

The expertise level of users who contributed images to the dataset is considered, and the dataset's worldwide distribution is visually displayed on a map, highlighting its global coverage and diversity.

<img src="https://github.com/dataset-ninja/surgical-scene-segmentation-in-robotic-gastrectomy/assets/78355358/0f628cbf-3151-4647-a65c-54b2197f023a" alt="image" width="800">

## Categories

The dataset distinguishes between 124 visual object categories, mostly pertaining to a street-level scene domain. The categories are organized into 7 (+1) root-level groups, namely ***object***, ***construction***, ***human***, ***marking*** (+***marking-only***), ***nature***, ***void***, and ***animal***. Each root-level group is organized into different macro-groups.


| root-level   | macro-level |          |               |              |         |       |
| :------------- | ------------- | ---------- | --------------- | :------------- | --------- | ------- |
| object       | sign        | support  | traffic-light | traffic-sign | vehicle | water |
| construction | barrier     | flat     | structure     |              |         |       |
| human        | person      | rider    |               |              |         |       |
| marking      | continous   | discrete | arrow         | hatched      | symbol  |       |
| marking-only | continous   | discrete |               |              |         |       |
| nature       |             |          |               |              |         |       |
| void         |             |          |               |              |         |       |
| animal       |             |          |               |              |         |       |

## Image Annotation

Image annotation was conducted by a team of 69 professional image annotators, delivering an average rate of approximately 5.1 images per annotator per day. The average annotation time is around 94 minutes per image. The annotation protocol was designed for each object category with systematic instructions and fallback annotation solutions.

## Quality Assurance

The dataset follows a two-stage quality assurance (QA) process targeting instance-specific annotation accuracies with precision and recall both greater than or equal to 97%. The first round of QA is applied to each image and is conducted as a follow-up step after annotation to correct potential mislabeling in terms of precision and recall. The second QA process is guided by a modified variant of the four-eyes principle.

## Dataset Splitting

The dataset is split into *training*, *validation*, and *test* sets. Training and validation data comprise 18,000 and 2,000 images, respectively, and the remaining 5,000 images form the test set. Each of the sets is additionally grouped by geographical regions. In such a way, segmentation assessment can be performed on more regional levels, potentially revealing classifier discrepancies e.g. when comparing results on images from North America to Asia.

## Statistical Analysis

The dataset is diverse in terms of image resolution, focal length, and camera model. It spans all the continents except for Antarctica, indicating a rich variety of images from different parts of the world. The dataset also contains a large number of object instances, making it suitable for fine-grained segmentation tasks.

All images are at least FullHD, but we have images with more than 22 Mpixels. Most pictures are in landscape orientation. The dominant aspect ratio is 4:3, followed by 16:9, but also other ratios are represented (mean ratio is 1.38). The mode of the distribution is at about 35 000 uploaded images with 50 users.

<img src="https://github.com/dataset-ninja/surgical-scene-segmentation-in-robotic-gastrectomy/assets/78355358/dfec3c52-e3f4-4a5b-950b-ebb40678ee5c" alt="image" width="400">

<span style="font-size: smaller; font-style: italic;">Top-left. Distribution of image resolution. Minimum size is fixed at Full HD (bottom left) and maximum image resolution is >22 MPixels. Top-right. Focal length distribution. Bottom. Distribution of camera sensors/devices used for image capturing.</span>

There is a predominance of mobile devices from Apple and Samsung, but in general the dataset spans a wide range of different camera types, also head- or car-mounted ones like Garmin and GoPro.
