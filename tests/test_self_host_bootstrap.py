from omni.self_host_bootstrap import plan_bootstrap


def test_bootstrap_plan_contains_self_rebuild():
    plan=plan_bootstrap()
    assert "rebuild-with-omni" in plan.stages
    assert "backend" in plan.units
