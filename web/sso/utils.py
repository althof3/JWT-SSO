from .models import Profile
import json
import os

def update_profile(user, attributes):
    mapping = {
        'nama': 'name',
        'npm': 'npm',
        'email': 'email',
        'peran_user': 'role',
        'kd_org': 'org_code',
    }

    updates = {mapping[key]: value for key, value in attributes.items() if key in mapping}
    data = {key: value for key, value in attributes.items() if key not in mapping}

    profile, created = Profile.objects.update_or_create(
        user=user,
        defaults=updates
    )

    data_json = json.loads(profile.data)
    data_json.update(data)
    profile.data = json.dumps(data_json)

    profile.save()

# cas 2
def get_ui_org_details(user, lang="id"):
    with open(os.path.join(os.path.dirname(__file__), 'ui_org.json')) as org_file:
        data = json.load(org_file)
        code = user.profile.org_code
        return data[lang][code]
