from ninja import Router
from ..models import User, Team
from ..schema import TeamAssing, TeamResponse, TeamOut, TeamIn
from typing import List

router = Router()

@router.get("/todos", response=List[TeamOut])
def get_teams(request):
    return Team.objects.all()

@router.post("/criar", response=TeamResponse, auth=None)
def create_team(request, team: TeamIn):
    t = Team.objects.create(team_name= team.team_name)
    t.save()
    
    return {"mensagem": "Team cadastrado"}


@router.post("/adicionar_usuario/", response=TeamResponse, auth=None)
def add_user_team(request, data: TeamAssing):
    try:
        team = Team.objects.get(team_id=data.team_id)
    except Team.DoesNotExist:
        return {"mensagem": "Equipe não encontrada"}
    
    membro = User.objects.filter(user_id__in=data.user_id)
    for team_member in membro:
        team.team_member.add(team_member)
    
    return {"mensagem": "Usuarios foram adicionados"}
        

@router.get("/pesquisar/{team_id}", response=TeamOut)
def search_team(request, team_id: int):
    team_data = Team.objects.get(team_id=team_id)
    return team_data

@router.put("/modificar/{team_id}", response=TeamOut)
def modify_team(request, team_id: int, team: TeamIn):
    team_data = Team.objects.get(team_id=team_id)
      
    for key, value in team.dict().items():
        setattr(team_data, key, value)
    team_data.save() 
    return team_data

@router.delete("/deletar/{team_id}")
def delect_team(request, team_id: int):
    team_data = Team.objects.get(team_id=team_id)
    team_data.delete()
    return {"message": "Team deletado com sucesso"}
