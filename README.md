# Eventyse
## Membros e papéis
- [Gabriel Victor Carvalho Rocha](https://github.com/gabreuvcr) - `Desenvolvedor FullStack`
- [Guilherme Bezerra dos Santos](https://github.com/guilhermebezerrads) - `Desenvolvedor FullStack`
- [Lucas Mariani Paiva Caldeira Brant](https://github.com/lucasbrant) - `Desenvolvedor FullStack`
- [Matheus Henrique Antunes Lima](https://github.com/motheuslima) - `Desenvolvedor FullStack`
 
## Funcional
**Objetivo**: Eventyse é uma rede social para o compartilhamento de roteiros de viagens. O principal objetivo é fazer com que viagens se tornem mais interessantes e mais proveitosas, visitando pontos de interesses previamente sugeridos por outros usuários, podendo ou não possuir uma ordem pré-definida. Os roteiros podem ser privados, guardando para uso futuro ou compartilhamento com conhecidos, ou podem ser públicos, permitindo comentários e avaliações de outros usuários que o experimentaram.
 
**Principais features**: 
* Criação de roteiros;
* Gerenciamento de roteiros, podendo editá-los ou excluí-los;
* Autenticação de usuários;
* Permitir deixar um roteiro privado ou público;
* Comentários em roteiros públicos;
* Salvar roteiros de outros usuários em uma coleção.
 
## Tecnologias
**Backend**: Python, usando Flask como framework  
**Frontend**: HTML, CSS e Angular (framework de JavaScript)  
**Banco de dados**: MySQL

## Backlog do Produto

* Como usuário, eu gostaria de ser capaz de criar uma conta para poder compartilhar meus roteiros;
* Como usuário, eu gostaria de seguir outros usuários para conseguir acompanhar seus roteiros;
* Como usuário, eu gostaria de ser capaz de criar um roteiro para conseguir compartilhar com outros usuários;
* Como usuário, eu gostaria de comentar roteiros de outros usuários para mostrar minha opinião;
* Como usuário, eu gostaria de visualizar roteiros de usuários que eu sigo para acompanhar apenas conhecidos;
* Como usuário, eu gostaria de avaliar roteiros de outros usuários para engajar e mostrar meu apoio;
* Como usuário, eu gostaria de ser capaz de realizar uma busca de roteiros em uma determinada cidade para poder encontrar os roteiros mais facilmente;
* Como usuário, eu gostaria de poder definir minhas rotas como públicas ou privadas, para preservar minha privacidade;
* Como usuário, eu gostaria de enviar uma mensagem a um outro usuário, para que possamos nos comunicar;
* Como usuário, eu gostaria de copiar um roteiro e adicionar outros pontos de interesse, para modificar rotas que me interassam;
* Como usuário, eu gostaria de poder combinar duas ou mais roteiros de outros usuários, para incrementar minhas rotas;
* Como usuário, eu gostaria de adicionar fotos e vídeos a minha postagem, para aprimorar a qualidade do post;
* Como usuário, eu gostaria de fazer login utilizando outras contas (Google, Facebook, etc) para integrar minhas contas já existentes;
* Como usuário, eu gostaria de favoritar roteiros de outros usuários para poder vê-los no futuro;

## Tarefas Técnicas
- Preparar o ambiente de desenvolvimento Front [Matheus] 
- Preparar o ambiente de desenvolvimento Back [Gabriel] 
- Criar e preparar o esquema do banco de dados [Lucas]
- Preparar o ambiente de deploy [Guilherme]

## Backlog da Sprint

**Como usuário, eu gostaria de ser capaz de criar uma conta para poder compartilhar meus roteiros:**
- Criar tela de Login [Lucas] 
- Criar tela de Cadastro [Matheus] 
- Criar tela de Perfil de Usuário [Guilherme] 
- Criar esquema Usuário [Lucas] 
- Criar serviço de Autenticação [Gabriel, Guilherme] 
- Criar controle Usuário (get/post) [Gabriel]

**Como usuário, eu gostaria de seguir outros usuários para conseguir acompanhar seus roteiros:**
- Criar botão seguir no perfil de um usuário [Matheus] 
- Criar rotas CreateSeguidor e RemoveSeguidor para adicionar e remover seguidores [Gabriel] 
- Criar rota GetSeguidor para recuperar seguidores de um usuário [Gabriel] 
- Criar métodos para adicionar e remover um seguidor [Guilherme] 
- Exibir seguidores e seguindo no perfil de um usuário [Matheus]

**Como usuário, eu gostaria de ser capaz de criar um roteiro para conseguir compartilhar com outros usuários:**
- Criar integração com Google Maps [Matheus]
- Criar componente de mapa [Matheus] 
- Permitir adicionar pontos no mapa [Matheus] 
- Criar formulário de roteiro com mapa e descrição [Guilherme] 
- Criar rota CreatePostagem [Gabriel] 
- Criar esquema Postagem [Lucas] 
- Criar serviço Postagem [Gabriel]

**Como usuário, eu gostaria de comentar roteiros de outros usuários para mostrar minha opinião:**
- Criar campo para escrever comentários em um roteiro [Matheus] 
- Criar botão de postar um comentário [Lucas] 
- Exibir os comentários existentes em um roteiro [Guilherme] 
- Criar botão de remover o próprio comentário [Lucas] 
- Criar rota GetComentarios para buscar os comentários de um roteiro [Lucas] 
- Criar rotas CreateComentario e RemoveComentario no controle Roteiro [Gabriel]

**Como usuário, eu gostaria de visualizar roteiros de usuários que eu sigo para acompanhar apenas conhecidos:**
- Pesquisar no banco roteiros recentes dos usuários que ele segue [Lucas] 
- Adicionar na página inicial uma linha do tempo com os roteiros dos usuários que o usuário segue [Lucas] 
- Criar rota GetRoteiros [Lucas]

**Como usuário, eu gostaria de avaliar roteiros de outros usuários para engajar e mostrar meu apoio:**
- Adicionar botões de Aprovo e Desaprovo [Guilherme] 
- Implementar rotas incrementaAprovo e incrementaDesaprovo [Guilherme]

**Como usuário, eu gostaria de ser capaz de realizar uma busca de roteiros em uma determinada cidade para poder encontrar os roteiros mais facilmente:**
- Adicionar campo de busca [Guilherme] 
- Adicionar front-end da página de resultados [Matheus] 
- Implementar rota buscaRoteiro [Gabriel]


Porta de entrada relacionado aos comentários
```py
from abc import ABC, abstractmethod
from domain.models.Comment import Comment

class ICommentService(ABC):
    @abstractmethod
    def create(self, username: str, roadmap_id: str, text: str) -> Comment:
        raise NotImplementedError

    @abstractmethod
    def find_all_by_roadmap_id(self, roadmap_id: str) -> list[Comment]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, username: str, comment_id: str) -> None:
        raise NotImplementedError
```

Adaptador REST que comunica com a porta de entrada ICommentService
```py
@inject.autoparams()
def create_comment_blueprint(comment_service: ICommentService) -> Blueprint:
    comments_blueprint = Blueprint('comments', __name__)
    
    @comments_blueprint.route('/comments/<roadmap_id>', methods=['POST'])
    @token_required
    def create_comment(current_user: User, roadmap_id: str):
        username: str = current_user.username
        text: str = request.json.get('text')

        comment: Comment = comment_service.create(username, roadmap_id, text)

        return comment.to_dict(), HTTPStatus.OK
    ...
```

##Wireframes

[Figma](https://www.figma.com/file/aGx9MIIJxTbHkNWAfBGFvA/Wireframe?node-id=0%3A1)
