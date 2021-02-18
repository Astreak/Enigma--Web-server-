class Config(object):
        DEBUG=True
        # Google_CLIENT_ID=''
        # {name}_CLIENT_SECRET=''
        # {name}_REQUEST_TOKEN_URL=''
        # {name}_REQUEST_TOKEN_PARAMS=''
        # {name}_ACCESS_TOKEN_URL=''
        # {name}_ACCESS_TOKEN_PARAMS=''
        # {name}_AUTHORIZE_URL=''
        # {name}_AUTHORIZE_PARAMS=''
        # {name}_API_BASE_URL=''
        # {name}_CLIENT_KWARGS
        
        

class ProductionEnv(Config):
        DEBUG=False
class DevelopmentEnv(Config):
        DEBUG=True
        SECRET_KEY="randomstring"
        SQLALCHEMY_DATABASE_URI="postgres://moqahhcw:k8K3m6W2EKoCkV03tP0_kYxcGjL4Ynev@ziggy.db.elephantsql.com:5432/moqahhcw"
        SQLALCHEMY_TRACK_MODIFICATIONS=True



