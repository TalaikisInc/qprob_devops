from .models import NetworkSite


def project_folders_helper():
    """Hardcoded version to create NetworkSite instances if no form available."""
    projects = ["bsnssnws", "entreprnrnws", "parameterless", "qprob", "realestenews", \
        "stckmrkt", "webdnl"]
    
    for proj in projects:
        try:
            ns = NetworkSite.objects.create(folder_name=proj)
            ns.save()
        except Exception as err:
            print(err)
    