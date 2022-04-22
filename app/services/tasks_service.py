from app.models.categories import CategoriesModel
from app.models.tasks import TasksModel


# TODO: fazer a criação das categorias que ainda não existem e separas das que já existem
# verificar se existe erro ao tentar criar uma categoria já existente ou se duplicara a categoria
# obs: nao pode duplicar categoria, então fazer verificação

def check_categories(payload):
    data_categories = payload.pop('categories')

    new_task = TasksModel(**payload)
    # print(new_task.categories)

    for categ in data_categories:
        # new_categ = CategoriesModel(name=categ)
        # new_task.categories.append(new_categ)
        
        # ERROR!!!
        # TODO: corrigir conceito se categoria deve ter elementos string ou 
        # do tipo CategoriesModel pelo Backref
        # new_task.categories.append(categ)
        ...

    # print(new_task.categories)
    
    return new_task
