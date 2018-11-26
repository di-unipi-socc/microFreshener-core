

def analyse_shared_persitency(micro_template):
    """Check the  presence of inapprorpiate service intimacy and shared persistency antipatterns"""
    for node in micro_template.databases:
        for r in  node.up_reup_requirements:
            print(r)
