"""Primary functions"""

import json

import click
import boto3

from user_map import UserMap


@click.command()
@click.option('--domain-id', help='Source Studio Domain ID for export')
@click.option('--filename', default='user_map.json',
              help='Filename of exported user mappings')
def export_user_map(domain_id: str, filename: str):
    sm_client = boto3.client('sagemaker')

    response = sm_client.list_user_profiles(
        DomainIdEquals=domain_id
    )
    user_profiles = response['UserProfiles']
    while response.get('NextToken') is not None:
        response = sm_client.list_user_profiles(
            NextToken=response['NextToken'],
            DomainIdEquals=domain_id
        )
        user_profiles += response['UserProfiles']

    user_maps = list()
    for profile in user_profiles:
        response = sm_client.describe_user_profile(
            DomainId=domain_id,
            UserProfileName=profile['UserProfileName']
        )
        user = UserMap(
            response['UserProfileName'],
            response['HomeEfsFileSystemUid'],
            sso_user_identifier=response['SingleSignOnUserIdentifier'],
            sso_user_value=response['SingleSignOnUserValue']
        )
        user_maps.append(user)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dumps(
            [user_map.asdict() for user_map in user_maps],
            f,
            ensure_ascii=False,
            indent=4
        )


@click.command()
def create_migration():
    pass


@click.command()
def execute_migration():
    pass
