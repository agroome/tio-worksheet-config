class Command:
    def __init__(self, tio, command, data_model):
        self.command = command
        self.data_model = data_model
        
        # Data models that work with this command type must specify a tio api_type, i.e. 'users'
        try:
            self.api_type = getattr(data_model, 'api_type')
        except AttributeError as e:
            raise AttributeError("model missing class variable: 'api_type'")

        # Get the API class, i.e. tio.users
        try:
            self.tio_api_class = getattr(tio, self.api_type)
        except AttributeError as e:
            raise NotImplementedError(f'[tio.{self.api_type}]: not a valid TenableIO api class')
        
        # Get the API class method, i.e. tio.users.create
        try:
            self.api_method = getattr(self.tio_api_class, command)
        except:
            raise NotImplementedError(f'[tio.{self.api_type}.{command}]: not a valid TenableIO.{self.api_type} method')
                
    def execute(self):
        parameters = self.data_model.dict()
        return self.api_method(**parameters)


class UserCommand(Command):
    def execute(self):
        parameters = self.data_model.dict(exclude={'groups'})
        print(parameters)
        return self.api_method(**parameters)