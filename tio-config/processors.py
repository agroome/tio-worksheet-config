from collections import defaultdict
from session import get_cached


def expand_users_with_groups(objects, action='create'):
    tio_groups = get_cached('groups')
    
    users = list(objects) # consider records may be a generator
    membership = defaultdict(list)
    group_index = {}

    if action == 'create':
        for user in users: 
            print(f'{action.upper}: {user.username}')
            user.action = action
            for group in user.groups:
                group_index[group.name] = group
                membership[group.name].append(user)
            yield user

        # commands to add groups 
        for group_name, group in group_index.items():
            if group_name not in tio_groups:
                if action == 'create':
                    group.action = action
                    yield group

        # commands to modify group membership
        for group_name, members in membership.items():
            usernames = sorted([u.username for u in members])
            group = group_index[group_name]
            group.action = 'add_user'
            for member in members:
                yield group
    
    # elif action == 'delete':
    #     for user in users: 
    #         print(f'{action.upper}: {user.username}')
    #         user.action = action
    #         try:
    #             user.id = tio_users[user.username]['id']
    #             yield user
    #         except IndexError as e:
    #             print(f"warning '{user.username}: trying to delete user that doesn't exist")