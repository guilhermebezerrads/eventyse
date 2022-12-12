context('EVENTYSE TESTS', () => {
    beforeEach(() => {
      cy.intercept('POST', '**/api/register', { fixture: 'register.mock.json' })
      cy.intercept('POST', '**/api/login', { fixture: 'register.mock.json' })
      cy.intercept('POST', '**/api/roadmaps', { fixture: 'create-post.mock.json' })
      cy.intercept('GET', '**/api/roadmaps', { fixture: 'post.mock.json' })
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
})
