import pytest
from app.users.dao import UsersDAO


@pytest.mark.parametrize('user_id, email, exist', [
    (1, 'test@test.com', True),
    (2, 'artem@example.com', True),
    (3, 'fake@fake.com', False)
])
async def test_find_by_id(user_id, email, exist):
    response = await UsersDAO.find_one_or_none(id=user_id)
    if exist:
        assert response.id == user_id
        assert response.email == email
    else:
        assert not response
