from omni.digital import DigitalSpec


def test_multimedia_is_an_open_world_digital_entity():
    spec = DigitalSpec(
        kind="multimedia.video",
        name="future-film",
        format="future-video-format",
        media={"codec": "future-codec", "duration": 120},
        metadata={"title": "A future digital work"},
    )
    spec.validate()
    data = spec.to_dict()
    assert data["kind"] == "multimedia.video"
    assert data["format"] == "future-video-format"
    assert data["media"]["codec"] == "future-codec"


def test_unknown_digital_entity_kind_remains_supported():
    spec = DigitalSpec(kind="future.multimedia.entity", name="new-format")
    spec.validate()
    assert spec.to_dict()["kind"] == "future.multimedia.entity"
