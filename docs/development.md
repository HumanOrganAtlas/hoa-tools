# Development

## Updating the inventory

After each HOA data release the inventory in this package needs updating.
To generate an updated inventory, run the [scripts/hoa/update_hoa_inventory.py script](https://github.com/HiPCTProject/hipct-data-tools/blob/main/scripts/hoa/update_hoa_inventory.py) in `hipct-data-tools`.
Then copy the output .csv file to src/hoa_tools/data/hoa_inventory.csv and commit the result.

## Generating the data model

Using [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator/):

```
datamodel-codegen --input src/hoa_tools/data/metadata/metadata-schema.json --input-file-type jsonschema --output src/hoa_tools/_hoa_model.py --output-model-type pydantic_v2.BaseModel --use-annotated --enum-field-as-literal all --use-union-operator --use-standard-collections
```
