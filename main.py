import streamlit as st
import time

class QuizApp:
    def __init__(self):
        # Inicializa o estado da sessão
        if 'user_name' not in st.session_state:
            st.session_state.user_name = ""
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'question_index' not in st.session_state:
            st.session_state.question_index = 0
        if 'quiz_started' not in st.session_state:
            st.session_state.quiz_started = False
        if 'responses' not in st.session_state:
            st.session_state.responses = []
        if 'start_time' not in st.session_state:
            st.session_state.start_time = 0  # Tempo de início para cada resposta
        if 'total_time' not in st.session_state:
            st.session_state.total_time = 0  # Tempo total gasto
        if 'timer_expired' not in st.session_state:
            st.session_state.timer_expired = False
        
        # Carrega as perguntas
        self.questions = self.load_questions()

        # Pergunta o nome do usuário
        if not st.session_state.quiz_started:
            st.session_state.user_name = st.text_input("Por favor, insira seu nome:", st.session_state.user_name)
            start_quiz_button = st.button("Iniciar Quiz")
            
            if start_quiz_button and st.session_state.user_name:
                st.session_state.quiz_started = True
                self.display_quiz()

        elif st.session_state.quiz_started:
            self.display_quiz()

    def load_questions(self):
        return [
            {"question": "1. CERA CARNAÚBA HYBRID OFERECE PROTEÇÃO CONTRA RAIOS UV?", "options": ["Verdadeiro", "Falso"], "answer": "Verdadeiro"},
            {"question": "2.	LIMPA VIDROS GLAZY DEIXA MANCHAS OU RESÍDUOS APÓS A APLICAÇÃO CORRETA?", "options": ["Verdadeiro", "Falso"], "answer": "Falso"},
            {"question": "3.	O PNEU PRETINHO VINTEX NÃO OFERECE PROTEÇÃO CONTRA OS RAIOS UV?", "options": ["Verdadeiro", "Falso"], "answer": "Falso"},
            {"question": "4.	QUAL PRODUTO MAIS INDICADO PARA REMOVER MANCHAS DE ÁGUA OU CALCIFICAÇÃO NOS VIDROS?", "options": ["PRIZM", "VIDREXX MAX", "GLAZY", "VIBREXX"], "answer": "PRIZM"},
            {"question": "5.	QUAL PRODUTO É IDEAL PARA LIMPEZA DE MOTOS?", "options": ["MOTO-V", "V-MOL"], "answer": "MOTO-V"},
            {"question": "6.	PARA REMOÇÃO DE PICHE E COLA INDICAMOS DELET", "options": ["VERDADEIRO", "FALSO"], "answer": "FALSO"},
            {"question": "7.	HIGICOURO PODE SER UTILIZADO APENAS NA LIMPEZA DE COURO NATURAL, E NÃO PODE SER APLICADO EM COURO SINTÉTICO.", "options": ["VERDADEIRO", "FALSO"], "answer": "FALSO"},
            {"question": "8.	RESTAURAX RENOVA E RESTAURA SUPERFÍCIES PLÁSTICAS, COMO PARA-CHOQUES, PAINÉIS E LATERAIS DE PORTAS.", "options": ["VERDADEIRO", "FALSO"], "answer": "VERDADEIRO"},
            {"question": "9.	QUAL DESSES PRODUTOS RECUPERA FARÓES QUE SOFRERAM OXIDAÇÃO COM O PASSAR DO TEMPO?", "options": ["V-LIGHT", "NATIVE","HIBRID WAX", "GLAUDIUS "], "answer": "V-LIGHT"},
            {"question": "10.	ALUMAX É UM DESENCRUSTANTE ÁCIDO PARA LIMPEZA DE GRAXAS E REMOÇÃO DE BARROS.", "options": ["VERDADEIRO", "FALSO"], "answer": "VERDADEIRO"},
            {"question": "11.	SINTRA PRO É UM LIMPADOR BACTERICIDA?", "options": ["VERDADEIRO", "FALSO"], "answer": "VERDADEIRO"},
            {"question": "12.	V-ECO VONIXX É A LINHA ECOLÓGICA QUE LAVA A SECO", "options": ["VERDADEIRO", "FALSO"], "answer": "VERDADEIRO"},
            {"question": "13.	MARQUE A ALTERNATIVA QUE TENHA SOMENTE LAVA AUTOS.", "options": ["CITRON, V-FLOC, V-MOL", "CITRON, V-FLOC, MOTO-V", "CITRON, SINTRA, MOTO-V", "CITRON, V-LUB, MOTO-V"], "answer": "CITRON, V-FLOC, V-MOL"},
            {"question": "14.	O PRODUTO DELET É UM LIMPADOR DE PNEUS E BORRACHAS?", "options": ["VERDADEIRO", "FALSO"], "answer": "VERDADEIRO"},
            {"question": "15.	O PRODUTO IZER É UM DESCONTAMINANTE FERROSO, NÃO RETIRA FERRUGEM.", "options": ["VERDADEIRO", "FALSO"], "answer": "VERDADEIRO"}
            ]

    def display_quiz(self):
        question_index = st.session_state.question_index
        questions = self.questions
        
        if question_index < len(questions):
            question = questions[question_index]
            st.write(question["question"])

            selected_option = st.radio("Escolha uma opção:", question["options"], key=f"option_{question_index}")
            submit_button = st.button("Enviar Resposta", key=f"submit_{question_index}")

            # Inicia o cronômetro de 40 segundos
            if st.session_state.start_time == 0:
                st.session_state.start_time = time.time()

            # Tempo limite para a resposta (40 segundos)
            time_remaining = 40 - (time.time() - st.session_state.start_time)

            if time_remaining > 0:
                st.write(f"Tempo restante: {int(time_remaining)} segundos")
            else:
                st.session_state.timer_expired = True

            if submit_button or st.session_state.timer_expired:
                # Armazena a resposta do usuário ou marca como errada se o tempo expirou
                if not st.session_state.timer_expired:
                    st.session_state.responses.append((question["question"], selected_option))
                    # Verifica se a resposta está correta
                    if selected_option == question["answer"]:
                        st.session_state.score += 1
                        st.success("Resposta correta!")
                    else:
                        st.error("Resposta incorreta!")
                else:
                    st.session_state.responses.append((question["question"], "Tempo esgotado"))
                    st.error("Tempo esgotado! Resposta considerada incorreta.")
                
                # Calcula o tempo total gasto
                st.session_state.total_time += (time.time() - st.session_state.start_time)
                st.session_state.start_time = 0  # Reinicia o tempo para a próxima pergunta
                st.session_state.timer_expired = False
                
                # Avança para a próxima pergunta
                st.session_state.question_index += 1
                st.rerun()  # Recarrega a página para exibir a próxima pergunta

        else:
            self.end_quiz()

    def end_quiz(self):
        st.write("Quiz concluído!")
        st.write(f"Sua pontuação final: {st.session_state.score} de {len(self.questions)}")
        st.write(f"Tempo total gasto: {int(st.session_state.total_time)} segundos")
        st.write("Respostas:")
        for question, response in st.session_state.responses:
            st.write(f"{question}: {response}")

        # Salva as respostas do usuário em um arquivo .txt
        self.save_results()

        st.balloons()  # Mostra uma animação ao finalizar o quiz

    def save_results(self):
        with open("ranking.txt", "a") as f:
            f.write(f"Nome: {st.session_state.user_name}, Acertos: {st.session_state.score}, "
                    f"Tempo total: {int(st.session_state.total_time)} segundos\n")
        st.success("Resultados salvos com sucesso!")

if __name__ == "__main__":
    QuizApp()
