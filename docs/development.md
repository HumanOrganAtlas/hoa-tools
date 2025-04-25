# Development

## Updating the inventory

To update the version of the inventory, update the git submodule at `src/hoa_tools/data/metadata`.
The inventory is stored separately at https://github.com/HumanOrganAtlas/metadata-schemas.

Then update the Python data model using [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator/):

```
datamodel-codegen --input src/hoa_tools/data/metadata/metadata-schema.json --input-file-type jsonschema --output src/hoa_tools/metadata.py --output-model-type pydantic_v2.BaseModel --use-annotated --enum-field-as-literal all --use-union-operator --use-standard-collections
```
