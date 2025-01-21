################################################################################################################
# Funcoes - SGL 
################################################################################################################

def validar_data_recebimento(value):
    if value and 'data_efetiva_envio' in self.__dict__ and value < self.data_efetiva_envio:
        raise ValidationError(
            _('A data de recebimento no laboratório não pode ser anterior à data efetiva de envio.'),
            code='invalid_data_recebimento'
        )

def validar_data_liberacao(value):
    if value and 'data_recebimento_laboratorio' in self.__dict__ and value < self.data_recebimento_laboratorio:
        raise ValidationError(
            _('A data de liberação dos resultados não pode ser anterior à data de recebimento no laboratório.'),
            code='invalid_data_liberacao'
        )
