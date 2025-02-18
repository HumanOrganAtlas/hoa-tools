# generated by datamodel-codegen:
#   filename:  metadata-schema.json
#   timestamp: 2025-02-18T16:31:32+00:00

from __future__ import annotations

from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel


class Contributor(BaseModel):
    name: Annotated[str, Field(title="Name")]
    roles: Annotated[
        list[
            Literal[
                "Conceptualization",
                "Data curation",
                "Formal analysis",
                "Funding acquisition",
                "Investigation",
                "Methodology",
                "Project administration",
                "Resources",
                "Software",
                "Supervision",
                "Validation",
                "Vlisualization",
                "Writing - original draft",
                "Writing - review & editing",
            ]
        ],
        Field(
            description="Contributor role(s), following the Contributor Role Taxonomy (CReditT)",
            title="Roles",
        ),
    ]


class Data(BaseModel):
    shape: Annotated[
        list,
        Field(
            description="Array shape for dataset.",
            max_length=3,
            min_length=3,
            title="Shape",
        ),
    ]
    voxel_size_um: Annotated[
        float,
        Field(
            description="Isotropic size of a single voxel, in micrometers.",
            gt=0.0,
            title="Voxel size",
        ),
    ]
    gcs_url: Annotated[
        str,
        Field(
            description="URL to data in Google Cloud Storage. Starts with either n5:// or zarr:// to specify whether data is in N5 or OME-Zarr 0.4 format.",
            title="Google cloud storage URL",
        ),
    ]


class Age(RootModel[int]):
    root: Annotated[int, Field(description="Age in years at death.", ge=0, title="Age")]


class Weight(RootModel[float]):
    root: Annotated[
        float, Field(description="Weight in kg at death.", gt=0.0, title="Weight")
    ]


class Height(RootModel[float]):
    root: Annotated[
        float, Field(description="Height in cm at death.", gt=0.0, title="Height")
    ]


class Donor(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: Annotated[str, Field(description="Unique donor ID.", title="ID")]
    age: Annotated[
        Age | Literal["<18", ">18"] | None,
        Field(description="Age in years at death.", title="Age"),
    ] = None
    sex: Annotated[Literal["M", "F"] | None, Field(title="Sex")] = None
    weight: Annotated[
        Weight | None, Field(description="Weight in kg at death.", title="Weight")
    ] = None
    height: Annotated[
        Height | None, Field(description="Height in cm at death.", title="Height")
    ] = None
    cause_of_death: Annotated[str | None, Field(title="Cause of death")] = None
    date_of_death: Annotated[date | None, Field(title="Date of death")] = None
    medical_history: Annotated[str | None, Field(title="Medical history")] = None
    diabetes: Annotated[
        Literal["Type 2", "No", "Yes"] | None, Field(title="Diabetes history")
    ] = None
    hypertension: Annotated[
        Literal["Yes", "No"] | None, Field(title="Hypertension history")
    ] = None
    smoker: Annotated[
        Literal["Never", "Yes"] | None, Field(title="Smoking history")
    ] = None


class Proposal(BaseModel):
    proposal_number: Annotated[
        Literal["md1252", "md1290", "md1389"],
        Field(description="Proposal number.", title="Proposal Number"),
    ]
    title: Annotated[str, Field(description="Proposal title.", title="Title")]
    proposers: Annotated[
        list[str], Field(description="Proposal proposers.", title="Proposers")
    ]


class Registration(BaseModel):
    source_dataset: Annotated[
        str,
        Field(
            description="Name of dataset that is registered (this dataset).",
            title="Source Dataset",
        ),
    ]
    target_dataset: Annotated[
        str,
        Field(
            description="Name of dataset that this dataset is registered to.",
            title="Target Dataset",
        ),
    ]
    translation: Annotated[
        list,
        Field(
            description="Translation vector.",
            max_length=3,
            min_length=3,
            title="Translation",
        ),
    ]
    rotation: Annotated[
        float, Field(description="Rotation in degrees about z-axis", title="Rotation")
    ]
    scale: Annotated[
        float, Field(description="Isotropic scaling factor.", title="Scale")
    ]


class PostMortemIntervalHours(RootModel[float]):
    root: Annotated[
        float,
        Field(
            description="Interval between death and fixation, in hours.",
            ge=0.0,
            title="Post-mortem interval",
        ),
    ]


class Sample(BaseModel):
    organ: Annotated[
        Literal["heart", "kidney", "lung", "brain", "spleen"],
        Field(description="Organ name.", title="Organ"),
    ]
    organ_context: Annotated[
        str | None,
        Field(
            description="Human-readable context for location of the dataset within the whole organ. Only present for some zoom datasets.",
            examples=["upper_lobe", "left", "tumor"],
            title="Organ Context",
        ),
    ] = None
    post_mortem_interval_hours: Annotated[
        PostMortemIntervalHours | None,
        Field(
            description="Interval between death and fixation, in hours.",
            title="Post-mortem interval",
        ),
    ] = None
    fixation_method: Annotated[
        Literal["immersion", "perfusion"] | None,
        Field(description="Fixation preparation method.", title="Fixation Method"),
    ] = None
    fixation_medium: Annotated[
        str | None, Field(description="Fixation medium", title="Fixation Medium")
    ] = None
    organ_infilled: Annotated[bool | str | None, Field(title="Organ Infilled")] = None
    stabilisation_medium: Annotated[
        Literal["agar cubes", "crushed agar", "beads"] | None,
        Field(title="Stabilisation Medium"),
    ] = None
    degassing_method: Annotated[
        Literal["inline", "vacuum", "vacuum+inline"] | None,
        Field(title="Degassing Method"),
    ] = None
    scan_solvent: Annotated[
        Literal["formalin", "ethanol"] | None,
        Field(description="Scan medium solvent.", title="Scan Solvent"),
    ] = None
    scan_solvent_concentration: Annotated[
        float | None,
        Field(
            description="Scan medium solvent concentration in percent.",
            title="Solvent concentration",
        ),
    ] = None
    scan_temperature: Annotated[
        str | float | None,
        Field(
            description="Temperature during scan, in degees celsius (if a number).",
            title="Scan Temperature",
        ),
    ] = "room temperature"


class Energy(RootModel[float]):
    root: Annotated[
        float,
        Field(
            description="Energy used during the scan, measured in keV.",
            gt=0.0,
            title="Energy",
        ),
    ]


class CurrentStart(RootModel[float]):
    root: Annotated[
        float,
        Field(
            description="Current of the synchrotron at the start of the scan, measured in mA.",
            gt=0.0,
            title="Current Start",
        ),
    ]


class NFrames(RootModel[int]):
    root: Annotated[
        int,
        Field(
            description="Number of frames acquired during the scan.",
            gt=0,
            title="Number of frames",
        ),
    ]


class NRef(RootModel[int]):
    root: Annotated[
        int,
        Field(
            description="Number of reference images collected during the scan.",
            ge=0,
            title="Number of references",
        ),
    ]


class NDark(RootModel[int]):
    root: Annotated[
        int,
        Field(
            description="Number of dark images (without illumination) collected during the scan.",
            ge=0,
            title="Number of darks",
        ),
    ]


class LatencyTime(RootModel[float]):
    root: Annotated[
        float,
        Field(
            description="Inactive time between active sensor times, measured in seconds.",
            gt=0.0,
            title="Latency Time",
        ),
    ]


class ExposureTime(RootModel[float]):
    root: Annotated[
        float,
        Field(
            description="Exposure time of a single frame, measured in seconds. This is the sub-frame time multiplied by the number of sub-frames.",
            gt=0.0,
            title="Exposure Time",
        ),
    ]


class SubframeTime(RootModel[float]):
    root: Annotated[
        float,
        Field(
            description="Exposure time of a single sub-frame, measured in seconds.",
            gt=0.0,
            title="Subframe Time",
        ),
    ]


class NSubframes(RootModel[int]):
    root: Annotated[
        int,
        Field(
            description="Number of frames accumulated per exposure.",
            gt=0,
            title="Number of sub-frames",
        ),
    ]


class NScans(RootModel[int]):
    root: Annotated[
        int,
        Field(
            description="Total number of scans. For a helical scan this is always 1. For a zseries this is the total number of scans concatenated to make the full data volume.",
            gt=0,
            title="Number of scans",
        ),
    ]


class ScanTime(RootModel[float]):
    root: Annotated[
        float,
        Field(
            description="Total duration of a single scan in seconds.",
            gt=0.0,
            title="Scan Time",
        ),
    ]


class OpticMagnification(RootModel[float]):
    root: Annotated[
        float,
        Field(
            description="Magnification in the optical setup.",
            gt=0.0,
            title="Optic Magnification",
        ),
    ]


class DistanceSourceSample(RootModel[float]):
    root: Annotated[
        float,
        Field(
            description="Distance between the source and the sample, measured in millimeters.",
            gt=0.0,
            title="Source-sample distance",
        ),
    ]


class DistanceSampleDetector(RootModel[float]):
    root: Annotated[
        float,
        Field(
            description="Distance between the sample and the detector, measured in millimeters.",
            gt=0.0,
            title="Sample-detector distance",
        ),
    ]


class SensorRoiXSize(RootModel[int]):
    root: Annotated[
        int,
        Field(
            description="Number of pixels in the x-dimension of the sensor's region of interest (ROI).",
            gt=0,
            title="Sensor Roi X Size",
        ),
    ]


class SensorRoiYSize(RootModel[int]):
    root: Annotated[
        int,
        Field(
            description="Number of pixels in the y-dimension of the sensor's region of interest (ROI).",
            gt=0,
            title="Sensor Roi Y Size",
        ),
    ]


class SensorBinning(RootModel[list]):
    root: Annotated[
        list,
        Field(
            description="Pixel binning on the sensor.",
            max_length=2,
            min_length=2,
            title="Sensor Binning",
        ),
    ]


class XrayMagnification(RootModel[float]):
    root: Annotated[
        float,
        Field(
            description="Magnification of X-rays due to divergence between the source and detector.",
            gt=0.0,
            title="Xray Magnification",
        ),
    ]


class Scan(BaseModel):
    date: Annotated[
        date, Field(description="Date when the scan was performed.", title="Date")
    ]
    beamline: Annotated[
        Literal["BM05", "BM18"],
        Field(description="ESRF beamline where scan was performed.", title="Beamline"),
    ]
    energy: Annotated[
        Energy | None,
        Field(
            description="Energy used during the scan, measured in keV.", title="Energy"
        ),
    ] = None
    current_start: Annotated[
        CurrentStart | None,
        Field(
            description="Current of the synchrotron at the start of the scan, measured in mA.",
            title="Current Start",
        ),
    ] = None
    filling_mode: Annotated[
        Literal[
            "16 bunch",
            "7/8 multibunch",
            "uniform multibunch",
            "28*12+1 bunch",
            "4 bunch",
        ]
        | None,
        Field(
            description="Mode of filling used in the synchrotron storage ring.",
            title="Filling Mode",
        ),
    ] = None
    n_frames: Annotated[
        NFrames | None,
        Field(
            description="Number of frames acquired during the scan.",
            title="Number of frames",
        ),
    ] = None
    n_ref: Annotated[
        NRef | None,
        Field(
            description="Number of reference images collected during the scan.",
            title="Number of references",
        ),
    ] = None
    n_dark: Annotated[
        NDark | None,
        Field(
            description="Number of dark images (without illumination) collected during the scan.",
            title="Number of darks",
        ),
    ] = None
    latency_time: Annotated[
        LatencyTime | None,
        Field(
            description="Inactive time between active sensor times, measured in seconds.",
            title="Latency Time",
        ),
    ] = None
    exposure_time: Annotated[
        ExposureTime | None,
        Field(
            description="Exposure time of a single frame, measured in seconds. This is the sub-frame time multiplied by the number of sub-frames.",
            title="Exposure Time",
        ),
    ] = None
    subframe_time: Annotated[
        SubframeTime | None,
        Field(
            description="Exposure time of a single sub-frame, measured in seconds.",
            title="Subframe Time",
        ),
    ] = None
    n_subframes: Annotated[
        NSubframes | None,
        Field(
            description="Number of frames accumulated per exposure.",
            title="Number of sub-frames",
        ),
    ] = None
    scan_type: Annotated[
        Literal["helical", "zseries"],
        Field(description="Type of scan.", title="Scan Type"),
    ]
    scan_range: Annotated[
        float,
        Field(
            description="Angular range of a single scan in degrees.",
            gt=0.0,
            title="Scan Range",
        ),
    ]
    n_scans: Annotated[
        NScans | None,
        Field(
            description="Total number of scans. For a helical scan this is always 1. For a zseries this is the total number of scans concatenated to make the full data volume.",
            title="Number of scans",
        ),
    ] = None
    acquisition: Annotated[
        Literal["half", "quarter"] | None,
        Field(description="Type of tomographic acquisition.", title="Acquisition"),
    ] = None
    z_step: Annotated[
        float | None,
        Field(description="Displacement in millimeters between scans.", title="Z Step"),
    ] = None
    scan_time: Annotated[
        ScanTime | None,
        Field(
            description="Total duration of a single scan in seconds.", title="Scan Time"
        ),
    ] = None
    filters: Annotated[
        list[str] | None,
        Field(description="List of filters used during the scan.", title="Filters"),
    ] = None
    scintillator: Annotated[
        Literal[
            "LuAG:Ce 1000um",
            "LuAG:Ce 100um",
            "LuAG:Ce 100um, reflective",
            "LuAG:Ce 100um, lead glass meniscus",
            "LuAG:Ce 2000um",
            "LuAG:Ce 2000um, reflective",
            "Multi LuAG:Ce 2000um, reflective",
            "LuAG:Ce 200um",
            "LuAG:Ce 250um",
            "LuAG:Ce 250um, reflective",
            "LuAG:Ce 25um",
            "LuAG:Ce 50um",
            "LuAG:Ce 50um, reflective",
            "LuAG:Ce 500um",
            "LySO:Ce 8.5um",
            "LySO:Ce 23um",
            "Gadox 60um",
            "CSI trixell structured 650um, 5um pitch",
            "GGG 8um",
            "gagg1000_refl",
            "dual-lso5000_refl",
        ]
        | None,
        Field(
            description="Scintillator used for converting X-rays to visible light.",
            title="Scintillator",
        ),
    ] = None
    optic: Annotated[
        Literal[
            "Zoom",
            "DZoom",
            "10x 0.4NA reflective optic",
            "Hasselblad tandem optic 100mm/300mm",
            "Hasselblad revolved 100 100",
            "LAFIP2 optic with canon 50mm",
            "Fixed x2",
            "Fixed x1",
            "Fixed x0.125",
            "Fixed x0.1",
            "Fixed x2.85",
            "Fixed x10",
            "Twinmic 5",
            "Twinmic 10",
            "Twinmic 20",
            "Triplemic 10",
        ]
        | None,
        Field(description="Optical components used during the scan", title="Optic"),
    ] = None
    optic_magnification: Annotated[
        OpticMagnification | None,
        Field(
            description="Magnification in the optical setup.",
            title="Optic Magnification",
        ),
    ] = None
    distance_source_sample: Annotated[
        DistanceSourceSample | None,
        Field(
            description="Distance between the source and the sample, measured in millimeters.",
            title="Source-sample distance",
        ),
    ] = None
    distance_sample_detector: Annotated[
        DistanceSampleDetector | None,
        Field(
            description="Distance between the sample and the detector, measured in millimeters.",
            title="Sample-detector distance",
        ),
    ] = None
    sensor_name: Annotated[
        Literal["PCO edge 4.2 CLHS", "Iris15"] | None,
        Field(
            description="Name of the sensor used during the scan.", title="Sensor Name"
        ),
    ] = None
    sensor_mode: Annotated[
        Literal["rolling shutter", "FFM"] | None,
        Field(
            description="Operating mode of the sensor during the scan.",
            title="Sensor Mode",
        ),
    ] = None
    sensor_roi_x_size: Annotated[
        SensorRoiXSize | None,
        Field(
            description="Number of pixels in the x-dimension of the sensor's region of interest (ROI).",
            title="Sensor Roi X Size",
        ),
    ] = None
    sensor_roi_y_size: Annotated[
        SensorRoiYSize | None,
        Field(
            description="Number of pixels in the y-dimension of the sensor's region of interest (ROI).",
            title="Sensor Roi Y Size",
        ),
    ] = None
    sensor_binning: Annotated[
        SensorBinning | None,
        Field(description="Pixel binning on the sensor.", title="Sensor Binning"),
    ] = None
    pixel_size: Annotated[
        float,
        Field(
            description="Size of a pixel at the sample, measured in micrometers.",
            gt=0.0,
            title="Pixel Size",
        ),
    ]
    xray_magnification: Annotated[
        XrayMagnification | None,
        Field(
            description="Magnification of X-rays due to divergence between the source and detector.",
            title="Xray Magnification",
        ),
    ] = None
    technique: Annotated[
        Literal["Hierarchical Phase-Contrast Tomography (HiP-CT)"],
        Field(title="Experimental technique."),
    ] = "Hierarchical Phase-Contrast Tomography (HiP-CT)"
    experiment_type: Annotated[str | None, Field(title="Experiment Type")] = (
        "Tomography"
    )


class Citation(BaseModel):
    title: Annotated[str, Field(description="Citation title", title="Title")]
    contributors: Annotated[
        list[Contributor],
        Field(
            description="Dataset contributors, listed alphabetically by name.",
            title="Contributors",
        ),
    ]
    doi: Annotated[str | None, Field(description="Dataset DOI", title="Doi")] = None
    author_list: Annotated[
        list[str],
        Field(
            description="Author list. If citing this data, please use this authorship list in the order given",
            title="Author List",
        ),
    ]


class HOAMetadata(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    name: Annotated[str, Field(description="Unique name for dataset.", title="Name")]
    dataset_type: Annotated[
        Literal["overview", "zoom"],
        Field(
            description="Type of dataset. Overview datasets contain the full sample. Zoom datasets contain a zoom into a particular volume of interest within the sample.",
            title="Dataset Type",
        ),
    ]
    voi: Annotated[
        str,
        Field(
            description="Volume of interest name. For zoom datasets this gives a unique identifier among zoom datasets taken within the same sample.",
            title="Volume of Interest",
        ),
    ]
    data: Annotated[Data, Field(description="Data metadata")]
    sample: Annotated[Sample, Field(description="Sample metadata")]
    donor: Annotated[Donor, Field(description="Donor metadata")]
    scan: Annotated[Scan, Field(description="Scan metadata")]
    proposal: Annotated[Proposal, Field(description="Beamtime proposal metadata")]
    registration: Annotated[
        Registration | None,
        Field(
            description="Metadata mapping high resolution volume of interest datasets to a full organ dataset. Not present for full organ datasets.",
            title="Registration parameters",
        ),
    ] = None
    citation: Annotated[Citation, Field(title="Dataset citation")]
