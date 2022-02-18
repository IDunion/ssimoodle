import os

def GetEnvVarOrDefault(envVar, default):
    ret = os.getenv(envVar)
    if ret:
        return ret
    else:
        return default

class Settings:
    serverAddress = GetEnvVarOrDefault("SERVER_ADDRESS", "0.0.0.0")
    serverPort = GetEnvVarOrDefault("SERVER_PORT", "9080")
    authToken = GetEnvVarOrDefault("X-AUTH-TOKEN", "SecretToken")
    databasePath = GetEnvVarOrDefault("DATABASE_PATH", "src/database")