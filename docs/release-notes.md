# Release notes

## 1.0.4

- Fixed a bug that prevented transforming VOIs between two datasets that
  are indirectly registered.

## 1.0.3

- Added the ability to transform between datasets that are indirectly registered,
  for example two zoom datasets that are registered to the same common overview dataset.
- Added [hoa_tools.dataset.Dataset.get_registered][] to get all datasets registered
  (directly or indirectly) to a given dataset.

## 1.0.2

- Fixed the inclusion of the metadata inventory in the distribution on PyPI.
- When a private copy of the metadata inventory is loaded, the registration
  inventory is now also updated correctly.

## 1.0.1

- Updated the metadata database to version 1.0. This has no major differences
  from the previous version of the metadata database (version 0.9).

## 1.0

First release of the `hoa-tools` package 🚀
