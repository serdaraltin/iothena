import uuid
import yaml

def generate_uuid():
    with open('config/statics.yaml', 'r') as f:
        config = yaml.safe_load(f)
        f.close()
    config['statics']['uuid'] = str(uuid.uuid4())
    with open('config/statics.yaml', 'w') as f:
        yaml.dump(config, f)
        f.close()

generate_uuid()