import { AppModule } from "../app.module";
import { LoginComponent } from "./login.component";

describe('LoginComponent', () => {
    beforeEach(() => {
        cy.mount(LoginComponent, {
            imports: [AppModule]
        })
    })

    it('has action disabled', () => {
        cy.get('button[id="login-action"]').should('be.disabled')
    })

    it('has action enabled after form filled', () => {
        cy.get('button[id="login-action"]').should('be.disabled')
        cy.get('input[id="login-mail"]').type("username0001_test")
        cy.get('input[id="login-password"]').type("username0001_test")
        cy.get('button[id="login-action"]').should('be.enabled')
    })
  })
