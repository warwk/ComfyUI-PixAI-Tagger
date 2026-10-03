import numpy as np
from PIL import Image

def process_tags(tagger_results, threshold, replace_underscore, remove):
    tags = []
    sorted_items = sorted(tagger_results.items(), key=lambda x: x[1], reverse=True)
    for item, score in sorted_items:
        if replace_underscore:
            item = item.replace("_", " ")
        item = item.replace("(", "\\(").replace(")", "\\)")
        if score > threshold and item.lower() not in remove:
            tags.append(item)
    return tags


class PixaiTagger:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "images": ("IMAGE", {"tooltip": "The input images to be tagged."}),
            "model": (
                    ["pixai-labs/pixai-tagger-v1.0"], 
                    {"default": "pixai-labs/pixai-tagger-v1.0", "tooltip": "The model to use for tagging. Currently pixai-labs/pixai-tagger-v1.0 is the only available model."}
                ),
            "threshold": (
                    "FLOAT", 
                    {"default": 0.17, "min": 0.0, "max": 1, "step": 0.05, "tooltip": "Threshold for general tags. Lower values will include more tags, higher values will be more selective. Default is 0.17."}
                ),
            "character_threshold": (
                    "FLOAT", 
                    {"default": 0.27, "min": 0.0, "max": 1, "step": 0.05, "tooltip": "Threshold for character tags. Lower values will include more tags, higher values will be more selective. Default is 0.27."}
                ),
            "replace_underscore": (
                    "BOOLEAN", 
                    {"default": False, "tooltip": "If enabled, underscores in tags will be replaced with spaces."}
                ),
            "trailing_comma": (
                    "BOOLEAN", 
                    {"default": False, "tooltip": "If enabled, a trailing comma will be added after the last tag."}
                ),
            "unload_model": (
                    "BOOLEAN", 
                    {"default": False, "tooltip": "If enabled, the model will be unloaded after tagging."}
                ),
            "exclude_tags": (
                    "STRING", 
                    {"default": "", "multiline": True, "tooltip": "A comma-separated list of tags to exclude from the results."}
                ),
        }}

    RETURN_NAMES = ("all_tags", )
    RETURN_TYPES = ("STRING", )
    OUTPUT_IS_LIST = (True, )
    FUNCTION = "tag"
    OUTPUT_NODE = True

    CATEGORY = "image"

    tagger = None
    loaded_model = ""

    def tag(self, images, model, threshold, character_threshold, replace_underscore=False, trailing_comma=False, unload_model=False, exclude_tags=""):
        tensor = images * 255
        tensor = np.array(tensor, dtype=np.uint8)
        remove = [s.strip() for s in exclude_tags.lower().split(",")]
        all_tags = []
        from transformers import pipeline
        
        # load pixai tagger model
        if self.loaded_model != model:
            self.tagger = pipeline(
                model=model,
                image_processor=model,
                trust_remote_code=True,
            )
            self.loaded_model = model
        
        # iterate through each image in the batch
        for i in range(tensor.shape[0]):
            image = Image.fromarray(tensor[i])
            results = self.tagger(image)["results"]

            _general = process_tags(results["general"], threshold, replace_underscore, remove)
            _character = process_tags(results["character"], character_threshold, replace_underscore, remove)
            _style = process_tags(results["style"], threshold, replace_underscore, remove)

            _all = _general + _character + _style
            all_tags.append(", ".join(_all))

            if trailing_comma:
                all_tags[-1] += ","

        if unload_model:
            self.tagger = None
            self.loaded_model = ""
        return (all_tags,)

class PixaiTaggerAdvanced:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "images": ("IMAGE", {"tooltip": "The input images to be tagged."}),
            "model": (
                    ["pixai-labs/pixai-tagger-v1.0"], 
                    {"default": "pixai-labs/pixai-tagger-v1.0", "tooltip": "The model to use for tagging. Currently pixai-labs/pixai-tagger-v1.0 is the only available model."}
                ),
            "character_threshold": (
                    "FLOAT", 
                    {"default": 0.27, "min": 0.0, "max": 1, "step": 0.05, "tooltip": "Threshold for character tags. Lower values will include more tags, higher values will be more selective. Default is 0.27."}
                ),
            "general_threshold": (
                    "FLOAT", 
                    {"default": 0.17, "min": 0.0, "max": 1, "step": 0.05, "tooltip": "Threshold for general tags. Lower values will include more tags, higher values will be more selective. Default is 0.17."}
                ),
            "style_threshold": (
                    "FLOAT", 
                    {"default": 0.15, "min": 0.0, "max": 1, "step": 0.05, "tooltip": "Threshold for style tags. Lower values will include more tags, higher values will be more selective. Default is 0.15."}
                ),
            "copyright_threshold": (
                    "FLOAT", 
                    {"default": 0.24, "min": 0.0, "max": 1, "step": 0.05, "tooltip": "Threshold for copyright tags. Lower values will include more tags, higher values will be more selective. Default is 0.24."}
                ),
            "meta_threshold": (
                    "FLOAT", 
                    {"default": 0.17, "min": 0.0, "max": 1, "step": 0.05, "tooltip": "Threshold for meta tags. Lower values will include more tags, higher values will be more selective. Default is 0.17."}
                ),
            "rating_threshold": (
                    "FLOAT", 
                    {"default": 0.41, "min": 0.0, "max": 1, "step": 0.05, "tooltip": "Threshold for rating tags. Lower values will include more tags, higher values will be more selective. Default is 0.41."}
                ),
            "replace_underscore": (
                    "BOOLEAN", 
                    {"default": False, "tooltip": "If enabled, underscores in tags will be replaced with spaces."}
                ),
            "unload_model": (
                    "BOOLEAN", 
                    {"default": False, "tooltip": "If enabled, the model will be unloaded after tagging."}
                ),
            "exclude_tags": (
                    "STRING", 
                    {"default": "", "multiline": True, "tooltip": "A comma-separated list of tags to exclude from the results."}
                ),
        }}

    RETURN_NAMES = ("character_tags", "general_tags", "style_tags", "copyright_tags", "meta_tags", "rating_tags")
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    OUTPUT_IS_LIST = (True, True, True, True, True, True)
    FUNCTION = "tag"
    OUTPUT_NODE = True

    CATEGORY = "image"

    tagger = None
    loaded_model = ""

    def tag(self, images, model, character_threshold, general_threshold, style_threshold, copyright_threshold, meta_threshold, rating_threshold, replace_underscore=False, unload_model=False, exclude_tags=""):
        tensor = images * 255
        tensor = np.array(tensor, dtype=np.uint8)
        remove = [s.strip() for s in exclude_tags.lower().split(",")]
        character_tags = []
        general_tags = []
        style_tags = []
        copyright_tags = []
        meta_tags = []
        rating_tags = []
        from transformers import pipeline
        
        # load pixai tagger model
        if self.loaded_model != model:
            self.tagger = pipeline(
                model=model,
                image_processor=model,
                trust_remote_code=True,
            )
            self.loaded_model = model
        
        # iterate through each image in the batch
        for i in range(tensor.shape[0]):
            image = Image.fromarray(tensor[i])
            results = self.tagger(image)["results"]

            _general =   process_tags(results["general"],   general_threshold, replace_underscore, remove)
            _character = process_tags(results["character"], character_threshold, replace_underscore, remove)
            _style =     process_tags(results["style"],     style_threshold, replace_underscore, remove)
            _copyright = process_tags(results["copyright"], copyright_threshold, replace_underscore, remove)
            _meta =      process_tags(results["meta"],      meta_threshold, replace_underscore, remove)
            _rating =    process_tags(results["rating"],    rating_threshold, replace_underscore, remove)

            general_tags.append(", ".join(_general))
            character_tags.append(", ".join(_character))
            style_tags.append(", ".join(_style))
            copyright_tags.append(", ".join(_copyright))
            meta_tags.append(", ".join(_meta))
            rating_tags.append(", ".join(_rating))

        if unload_model:
            self.tagger = None
            self.loaded_model = ""
        return (character_tags, general_tags, style_tags, copyright_tags, meta_tags, rating_tags)

