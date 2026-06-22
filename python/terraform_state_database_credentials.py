import json

state = json.load(open('terraform.tfstate'))


resources = []

for resource in state['resources']:
    if resource['type'] == 'aws_db_instance':
        instances = resource['instances']
        if len(instances) > 0:
            attributes = instances[0]['attributes']
            if attributes['engine'] == 'postgres':
                resources.append(attributes)
            if attributes['engine'] == 'mysql':
                resources.append(attributes)
    elif resource['type'] == 'aws_rds_cluster':
        instances = resource['instances']
        if len(instances) > 0:
            attributes = instances[0]['attributes']
            if attributes['engine'] == 'aurora-postgresql':
                resources.append({
                    'address': attributes['endpoint'],
                    'db_name': attributes['database_name'],
                    'password': attributes['master_password'],
                })

resources.sort(key=lambda resource: resource['address'])

for resource in resources:
    print({
        'host': resource['address'],
        'database': resource['db_name'],
        'password': resource['password'],
    })

print("\n\n")

for resource in resources:
    host = resource['address']
    database = resource['db_name']
    password = resource['password']
    print(f"postgres://root:{password}@{host}:5432/{database}")
