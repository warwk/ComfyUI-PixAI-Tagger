from .pixai_tagger import PixaiTagger, PixaiTaggerAdvanced

NODE_CLASS_MAPPINGS = {
    "PixAI Tagger": PixaiTagger,
    "PixAI Tagger Advanced": PixaiTaggerAdvanced,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PixAI Tagger": "PixAI Tagger",
    "PixAI Tagger Advanced": "PixAI Tagger (Advanced)",
}
