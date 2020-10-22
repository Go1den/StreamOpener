class Tag:
    def __init__(self, tag):
        self.id = tag["tag_id"]
        self.isAuto = tag["is_auto"]
        self.localizationNames = tag["localization_names"]
