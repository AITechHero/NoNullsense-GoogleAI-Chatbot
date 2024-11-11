import sys
import subprocess
import shutil

def check_requirements():
    checks = {
        'Python': {
            'command': ['python', '--version'],
            'min_version': '3.9.0'
        },
        'Node': {
            'command': ['node', '--version'],
            'min_version': 'v16.0.0'
        },
        'gcloud': {
            'command': ['gcloud', '--version'],
            'required': True
        }
    }
    
    results = []
    for tool, config in checks.items():
        if shutil.which(config['command'][0]):
            try:
                version = subprocess.check_output(config['command']).decode().strip()
                results.append(f'✅ {tool}: {version}')
            except:
                results.append(f'❌ {tool}: Error checking version')
        else:
            results.append(f'❌ {tool}: Not found')
    
    return results

if __name__ == '__main__':
    print('Checking environment setup...')
    for result in check_requirements():
        print(result)