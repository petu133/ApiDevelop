from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str  #(In development) all the variables are setting inside the .env file... 
    database_name: str      # not pushed to the source code repository by security reasons
    database_username: str  
    master_key: str         #(In production) these are going to be set on the machine environment
    algo: str
    token_expiration_min: int
    class Config:
        env_file = ".env"


settings = Settings()
# type_data = type(settings)
# print(f"The data contained in settings of type -{type_data}- is : {settings} ")


# class SettingsExample(BaseSettings): # Handles environment variables
#     database_password: str = "localhost" #set default value to localhost
#     database_url: str = "postgres"
#     secret_key: str = "5534uo34250j43j4"    