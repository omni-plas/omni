from omni.self_host import make_self_host_plan


def test_self_host_plan_has_bootstrap_and_native_stages():
    plan=make_self_host_plan()
    assert plan.stages==('bootstrap','native-compile','self-compile','replace-bootstrap')
