Dataset **Mapillary Vistas** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/k/P/XU/ey9D9NGgoGxpvWn8IOMWg8GpgsbcrjLVVWE8I14iIXg5rf1OQz6oEuTfzfCLcmPKJMsu6r0Vo4dGhl7cqdKe9G4pMS3SoqIIVtTBtRNRUMZBBy7PXxOM0KM750lp.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Mapillary Vistas', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.mapillary.com/dataset/vistas).