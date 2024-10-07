from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

from utils.logger import Logger


class Model:
    def __init__(self, analitics):
        self.logger = Logger()
        self.load_model()
        self.context = self.build_context(analitics)

    def load_model(self, model_name="deepset/bert-base-cased-squad2"):
        try:
            self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.nlp = pipeline('question-answering', model=self.model, tokenizer=self.tokenizer)
            self.logger.log_info(f"Model loaded successfully: {model_name}")
        except Exception as e:
            self.logger.log_error(f"Error loading model: {str(e)}")
            return False
        return True
    
    def build_context(self, analitics):
        try:
            best_p = analitics['best_p']
            old_eff_d = analitics['old_eff_d']
            new_eff_d = analitics['new_eff_d']
            short_rt = analitics['short_rt']
            long_rt = analitics['long_rt']
            context = f"""
                El proveedor más popular es {best_p[0]} porque tiene {best_p[1]}.\n
                La fecha efectiva más reciente es {new_eff_d[0]} del contrato {new_eff_d[1]}.\n
                El plazo de renovación más corto es {short_rt} días.\n
                El plazo de renovación más extenso es {long_rt} días.\n
                La fecha efectiva más antigua es {old_eff_d[0]}.
                """
            self.logger.log_info(f"Context built successfully")
        except Exception as e:
            self.logger.log_error(f"Error building context: {str(e)}")
            return False
        return context
    
    def ask_question(self, question):
        try:
            answer = self.nlp(question=question, context=self.context)
        except Exception as e:
            self.logger.log_error(f"Error asking question: {str(e)}")
            return False
        return answer['answer'].capitalize()