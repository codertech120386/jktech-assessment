from pydantic import BaseModel


class CreateLlamaSummarySchema(BaseModel):
    content: str

    class Config:
        json_schema_extra = {
            "example": {
                "content": """
                    This Contractor Agreement (“ A gre e me nt” ) is entered into
                     as of December 26, 2022 (the
                    “ E f f e c t i v e D a t e” ), between:
                    Omneky Inc, a C Corporation having its principal place of business/Headquarters
                    at 3357
                    26th St San Francisco 94110-4635 United States, email address: hi@omneky.com,
                    registered in United States under the number 82-4397148
                    (“ C l i e nt” ), and
                    Dhaval Chheda, an individual whose address is 1601, Vihang CHS, Siddharth Nagar Road
                    Number 4, Goregaon (W) Mumbai 400104 India, email address: dhaval@omneky.com, and
                    whose activity is registered in India
                    under the number AJEPC2911M
                    (“ C ont ra c t or” )
                    A. The Client is looking for a professional with the professional skills to carry out the
                    activities listed in the Statement of Work from time to time executed between the
                    Parties and attached hereto.
                    B. The Contractor declares that the Contractor possesses the necessary
                    professionalism, having gained considerable experience in the field and declares that
                    the Contractor is willing to carry out the activities listed in the Statement of Work that
                    the Client intends to entrust to the Contractor in total autonomy.
                    C. The Parties intend to establish a collaboration of an autonomous nature, both from a
                    formal and substantial perspective, excluding as of now any intervention by Client
                    regarding the modalities of performance and the time of execution of the Service to
                    be carried out and any exclusive obligation on the part of the Contractor.
                    D. The present Contract excludes any subjection to the power of direction or control of
                    the personnel with whom, by reason of the Service, the Contractor may come into
                    contact.
                    Client and Contractor desire to have Contractor perform services for Client, subject to and
                    in accordance with the terms and conditions of this Agreement.
                    NOW, THEREFORE, the parties agree as follows:
                """,
                "rating": 5,
            }
        }
