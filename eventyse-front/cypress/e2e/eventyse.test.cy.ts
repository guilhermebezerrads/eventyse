context('EVENTYSE TESTS', () => {
    beforeEach(() => {
      cy.intercept('POST', '**/api/register', { fixture: 'register.mock.json' })
      cy.intercept('POST', '**/api/login', { fixture: 'register.mock.json' })
      cy.intercept('POST', '**/api/roadmaps', { fixture: 'create-post.mock.json' })
      cy.intercept('GET', '**/api/roadmaps', { fixture: 'posts.mock.json' })
      cy.intercept('GET', '**/api/roadmaps/user/BCD', { fixture: 'post2.mock.json' })
      cy.intercept('GET', '**/api/roadmaps/user/ABC', { fixture: 'post.mock.json' })
      cy.intercept('POST', '**/api/comments/1', { fixture: 'comment.mock.json' })
      cy.intercept('GET', '**/api/comments/1', { fixture: 'comment.mock.json' })
      cy.intercept('DELETE', '**/api/comments/1', { fixture: 'comment.mock.json' })
      cy.intercept('GET', '**/api/users/BCD', { fixture: 'user2.mock.json' })
      cy.intercept('GET', '**/api/users/ABC', { fixture: 'user.mock.json' })
      cy.intercept('GET', '**/api/users/follow/BCD', { fixture: 'check-follow.mock.json' }),
      cy.intercept('PUT', '**/api/users/follow/BCD', { fixture: 'follow.mock.json' })
      cy.intercept('GET', '**/api/roadmaps/like/1', { fixture: 'check-like.mock.json' })
      cy.intercept('GET', '**/api/roadmaps/dislike/1', { fixture: 'check-like.mock.json' })
      cy.intercept('PUT', '**/api/roadmaps/like/1', { fixture: 'like.mock.json' })
      cy.intercept('PUT', '**/api/roadmaps/dislike/1', { fixture: 'like.mock.json' })
      cy.intercept('GET', '**/api/roadmaps/tag/tag1', { fixture: 'post2.mock.json' })
    })

    afterEach(() => {
        cy.wait(1000)
    })

    it('should be on login page', () => {
        cy.visit('localhost:4200/login')
        cy.location('pathname').should('include', 'login')
        cy.get('[id="signup-link-action"]').click()
        cy.location('pathname').should('include', 'signup')
    })

    it('should not allow login without form', () => {
        cy.visit('localhost:4200/login')
        cy.location('pathname').should('include', 'login')

        cy.get('button[id="login-action"]').should('be.disabled')
        cy.get('input[id="login-mail"]').type("username0001_test")
        cy.get('input[id="login-password"]').type("username0001_test")
        cy.get('button[id="login-action"]').should('be.enabled')
    })

    it('should not allow signup without form', () => {
        cy.visit('localhost:4200/login')
        cy.location('pathname').should('include', 'login')
        cy.get('[id="signup-link-action"]').click()
        cy.location('pathname').should('include', 'signup')

        cy.get('button[id="signup-action"]').should('be.disabled')
        cy.get('input[id="signup-mail"]').type("username0001_test")
        cy.get('input[id="signup-name"]').type("username0001_test")
        cy.get('input[id="signup-password"]').type("username0001_test")
        cy.get('button[id="signup-action"]').should('be.enabled')
    })

    it('should be on dashboard after signup', () => {
        cy.visit('localhost:4200/login')
        cy.get('[id="signup-link-action"]').click()
        cy.location('pathname').should('include', 'signup')

        cy.get('button[id="signup-action"]').should('be.disabled')
        cy.get('input[id="signup-mail"]').type("username0001_test")
        cy.get('input[id="signup-name"]').type("username0001_test")
        cy.get('input[id="signup-password"]').type("username0001_test")
        cy.get('button[id="signup-action"]').should('be.enabled')

        cy.get('button[id="signup-action"]').click()
    })

    it('should add a new post', () => {
        cy.visit('localhost:4200')

        cy.get('input[id="login-mail"]').type("username0001_test")
        cy.get('input[id="login-password"]').type("username0001_test")
        cy.get('button[id="login-action"]').click()

        cy.get('button[id="create-post-action"]').click()
        cy.location('pathname').should('include', 'create')

        cy.get('button[id="post-save-action"]').should('be.disabled')

        cy.wait(2000)

        cy.get('.map')
        .dblclick(390, 250)
        .dblclick(400, 50);

        cy.get('input[id="post-name"]').type("nome de uma postagem")
        cy.get('textarea[id="post-desc"]').type("descricao de uma postagem")

        cy.get('button[id="post-save-action"]').should('be.enabled')

        cy.get('input[id="post-tags"]').type("tag,tag2,tag3,")

        cy.get('button[id="post-save-action"]').click()
        cy.location('pathname').should('include', 'dashboard')
    })

    it('should load posts', () => {
        cy.visit('localhost:4200')

        cy.get('input[id="login-mail"]').type("username0001_test")
        cy.get('input[id="login-password"]').type("username0001_test")
        cy.get('button[id="login-action"]').click()

        cy.location('pathname').should('include', 'dashboard')
    })

    it('should comment on a post', () => {
        cy.visit('localhost:4200')

        cy.get('input[id="login-mail"]').type("username0001_test")
        cy.get('input[id="login-password"]').type("username0001_test")
        cy.get('button[id="login-action"]').click()

        cy.location('pathname').should('include', 'dashboard')

        cy.get('.comment-input').type("este comentario é apenas um teste")
        cy.get('.comment-action').click()
    })

    it('should comment on a post and then delete the comment', () => {
        cy.visit('localhost:4200')

        cy.get('input[id="login-mail"]').type("username0001_test")
        cy.get('input[id="login-password"]').type("username0001_test")
        cy.get('button[id="login-action"]').click()

        cy.location('pathname').should('include', 'dashboard')

        cy.get('.comment-input').type("este comentario é apenas um teste")
        cy.get('.comment-action').click()

        cy.wait(2000)

        cy.get('.delete-comment-action').click()
    })

    it('should go to profile', () => {
        cy.visit('localhost:4200')

        cy.get('input[id="login-mail"]').type("username0001_test")
        cy.get('input[id="login-password"]').type("username0001_test")
        cy.get('button[id="login-action"]').click()

        cy.get('button[id="avatar-action"]').click()
        cy.get('button[id="avatar-profile-action"]').click()

        cy.location('pathname').should('include', 'profile')
    })

    it('should follow other user profile', () => {
        cy.visit('localhost:4200')

        cy.get('input[id="login-mail"]').type("username0001_test")
        cy.get('input[id="login-password"]').type("username0001_test")
        cy.get('button[id="login-action"]').click()

        cy.wait(1000)
        cy.get('.post-author-link').click()

        cy.location('pathname').should('include', 'profile')

        cy.get('button[id="follow-action"]').click()
    })

    it('should like', () => {
        cy.visit('localhost:4200')

        cy.get('input[id="login-mail"]').type("username0001_test")
        cy.get('input[id="login-password"]').type("username0001_test")
        cy.get('button[id="login-action"]').click()

        cy.wait(1000)

        cy.get('.like-action').click()
    })

    it('should dislike', () => {
        cy.visit('localhost:4200')

        cy.get('input[id="login-mail"]').type("username0001_test")
        cy.get('input[id="login-password"]').type("username0001_test")
        cy.get('button[id="login-action"]').click()

        cy.wait(1000)

        cy.get('.dislike-action').click()
    })

    it('should filter post by tag', () => {
        cy.visit('localhost:4200')

        cy.get('input[id="login-mail"]').type("username0001_test")
        cy.get('input[id="login-password"]').type("username0001_test")
        cy.get('button[id="login-action"]').click()

        cy.wait(1000)

        cy.get('input[id="filter-input"]').type("tag1")
        cy.get('[id="filter-form"]').submit()

        cy.location('pathname').should('include', 'filterTag=tag1')
    })
})
