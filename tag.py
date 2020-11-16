class Tag:
    def __init__(self, tag=None, tagID=None, isAuto=None, localizationNames=None, isActive=None):
        if tag:
            self.id = tag["tag_id"]
            self.isAuto = tag["is_auto"]
            self.localizationNames = tag["localization_names"]
            self.isActive = True
        else:
            self.id = tagID
            self.isAuto = isAuto
            self.localizationNames = localizationNames
            self.isActive = isActive
