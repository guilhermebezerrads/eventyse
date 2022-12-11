import { AppModule } from "../app.module";
import { SignupComponent } from "./signup.component";

describe('SignupComponent', () => {
    beforeEach(() => {
        cy.mount(SignupComponent, {
            imports: [AppModule]
        })
    })

    it('has action disabled', () => {
        cy.get('button[id="signup-action"]').should('be.disabled')
    })

    it('has action enabled after form filled', () => {
        cy.get('button[id="signup-action"]').should('be.disabled')
        cy.get('input[id="signup-mail"]').type("username0001_test")
        cy.get('input[id="signup-name"]').type("username0001_test")
        cy.get('input[id="signup-password"]').type("username0001_test")
        cy.get('button[id="signup-action"]').should('be.enabled')
    })
  })
