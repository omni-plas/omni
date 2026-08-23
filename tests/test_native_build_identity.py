from omni.native_build_identity import BuildIdentity


def test_build_identity_has_three_stable_digests():
    ident=BuildIdentity.create('x86_64-linux-sysv',{'entry':'main'},b'ELF')
    assert ident.target=='x86_64-linux-sysv'
    assert len(ident.manifest)==64
    assert len(ident.artifact)==64
