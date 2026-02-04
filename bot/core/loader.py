from __future__ import annotations

import importlib
import logging
from typing import Dict, List

log = logging.getLogger(__name__)

def _command_qualified_keys(tree) -> set[str]:
    return {cmd.name for cmd in tree.get_commands()}

def load_features(tree, config: Dict) -> List:
    """Dynamically load and register features based on config, return dict of loaded modules and dict of failed ones with error messages

    Each feature module must be located at features/{slug}/feature.py and define:
    - a FEATURE dictionary with keys: slug, name, description, version, author, requires_config (bool), permissions (list of str)
    - a register(tree, config) function that registers the feature's commands to the provided tree using the provided config dict

    Parameters:
        tree: the app_commands.CommandTree to register commands to
        config: the full configuration dict loaded from the config file, used to pass feature-specific config to each module

    Returns:
        loaded: dict mapping feature slug to the imported module object for successfully loaded features
        failed: dict mapping feature slug to error message for features that failed to load
    """
    params_needed: List[str] = ["slug", "name", "description", "version", "author", "requires_config", "permissions"]
    enabled: List[str] = config["enabled_features"]
    features_config : Dict = config.get("features", {})
    
    loaded : Dict[str, object] = {}
    failed : Dict[str, str] = {}
    
    for slug in enabled:
        module_path = f"features.{slug}.feature"
        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            failed[slug] = "ImportError: " + str(e)
            log.error(f"Failed to import feature module {module_path}: {e}")
            continue
        
        if not hasattr(module, "FEATURE"):
            failed[slug] = "Missing FEATURE dictionary"
            log.error(f"Feature module {module_path} is missing FEATURE dictionary.")
            continue
        
        if not hasattr(module, "register"):
            failed[slug] = "Missing register function"
            log.error(f"Feature module {module_path} is missing register function.")
            continue
        
        feature_info : Dict = module.FEATURE
        
        if not isinstance(feature_info, dict):
            failed[slug] = "FEATURE is not a dictionary"
            log.error(f"Feature module {module_path} FEATURE is not a dictionary.")
            continue
        
        if not feature_info.get("slug"):
            failed[slug] = "FEATURE missing slug"
            log.error(f"Feature module {module_path} FEATURE dictionary missing slug.")
            continue
        
        if not all(param in feature_info for param in params_needed):
            missing_params = [param for param in params_needed if param not in feature_info]
            failed[slug] = "Missing parameters: " + ", ".join(missing_params)
            log.error(f"Feature module {module_path} FEATURE dictionary missing parameters: {', '.join(missing_params)}.")
            continue
        
        if feature_info.get("slug") != slug:
            failed[slug] = "Slug mismatch"
            log.error(f"Feature module {module_path} slug mismatch: expected {slug}, got {feature_info.get('slug')}.")
            continue
        
        feature_cfg : Dict = features_config.get(slug, {})
        
        if feature_info.get("requires_config", True) and not feature_cfg:
            failed[slug] = "Missing required configuration"
            log.error(f"Feature module {module_path} requires configuration but none was provided.")
            continue
            
        try:
            
            before = _command_qualified_keys(tree)
            log.debug(f"Commands before loading feature {slug}: {before}")
            module.register(tree, feature_cfg)
            
            after = _command_qualified_keys(tree)
            log.debug(f"Commands after loading feature {slug}: {after}")
            added = after - before
            duplicates = before & added
            if duplicates:
                failed[slug] = "Command name conflict: " + ", ".join(sorted(duplicates))
                log.error(f"Feature module {module_path} command name conflict: {', '.join(sorted(duplicates))}.")
                
                for cmd_name in added:
                    try:
                        tree.remove_command(cmd_name)
                    except Exception as e:
                        pass
                continue
            
            
            loaded[slug] = module
            log.info(f"Successfully loaded feature module {module_path}.")
        except Exception as e:
            failed[slug] = "RegistrationError: " + str(e)
            log.error(f"Failed to register feature module {module_path}: {e}")
        
    return loaded, failed