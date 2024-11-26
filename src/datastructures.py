"""
Implement the following methods:
- add_member: Adds a member to the self._members list
- delete_member: Deletes a member from the self._members list
- update_member: Updates a member from the self._members list
- get_member: Returns a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []

    # Generar id unicos
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        if "id" not in member:
            member["id"] = self._generate_id()
        member["last_name"] = self.last_name
        self._members.append(member)
        return member

    def delete_member(self, id):
        for position, member in enumerate(self._members):
            if member["id"] == id:
                self._members.pop(position)
                return True
        return False

    def update_member(self, id, updated_data):
        for member in self._members:
            if member["id"] == id:
                member.update(updated_data)
                return member
        return None

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    def get_all_members(self):
        return self._members
