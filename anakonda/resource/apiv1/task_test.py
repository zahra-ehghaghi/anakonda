import pytest

@pytest.mark.parametrize(
["status","code","headers","is_collection","task_id"],
(
    [400,105,{},True,""],
    [200,100,{"Content-Type":"application/json"},True,""],
    [400,105,{},False,"1"],
    #[404,107,{"Content-Type":"application/json"},False,"1"],
)

)
    


def test_get(client,status,code,headers,is_collection,task_id):
    
    if is_collection is True:
        result = client.get("/api/v1/tasks",headers = headers)
        print (result)
    else:
        result = client.get(f"/api/v1/tasks/{task_id}",headers = headers)
        print (result)
    assert result.status_code == status
    