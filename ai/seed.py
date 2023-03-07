import random
import sqlite3
import pickle
import os


class ChatbotDatabase:
    def __init__(self, database_name='chatbot.db'):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        self.create_tables()
        
    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS conversations 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             user_id TEXT, 
                             message TEXT,
                             response TEXT,
                             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        self.connection.commit()
    
    def add_conversation(self, user_id, message, response):
        self.cursor.execute("INSERT INTO conversations (user_id, message, response) VALUES (?, ?, ?)",
                            (user_id, message, response))
        self.connection.commit()
    
    def get_last_message(self, user_id):
        self.cursor.execute("SELECT message FROM conversations WHERE user_id=? ORDER BY timestamp DESC LIMIT 1",
                            (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

class ConversationBot:
    def __init__(self):
        self.db = ChatbotDatabase()
        self.context = None
        self.neural_network = None

        input_size = 50
        hidden_sizes = [100, 100]
        output_size = 100
        
        if isinstance(input_size, int) and all(isinstance(size, int) for size in hidden_sizes) and isinstance(output_size, int):
            self.neural_network = NeuralNetwork(input_size, hidden_sizes, output_size)
        else:
            raise ValueError("Invalid input or output size.")
        
    def load_model(self, filename):
        if not os.path.exists(filename):
            self.save_model(filename)  # Create the file if it doesn't exist
        with open(filename, 'rb') as file:
            self.neural_network = pickle.load(file)
            
    def save_model(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.neural_network, file)
        
    def load_database(self, db_file):
        self.db = ChatbotDatabase(db_file)
        
    def __del__(self):
        self.conn.close()
        
    def add_node(self):
        layer = random.randint(0, len(self.neural_network.weights) - 2)
        self.neural_network.add_node(layer)
    
    def train(self, epochs=10):
        if self.training_data:
            for i in range(epochs):
                for input_data, output_data in self.training_data:
                    self.neural_network.train(input_data, output_data)
            print("Bot trained successfully!")
        else:
            print("No training data available!")
            
    def add_training_data(self, input_data, output_data):
        self.training_data.append((input_data, output_data))
        self.c.execute("INSERT INTO conversation_history (input, output, context) VALUES (?, ?, ?)",
                      (input_data, output_data, self.context))
        self.conn.commit()
    
    def get_response(self, input_data):
        # Use context tracking to personalize responses
        if self.context:
            history_query = "SELECT output FROM conversation_history WHERE context=? ORDER BY RANDOM() LIMIT 1"
            self.c.execute(history_query, (self.context,))
            history = self.c.fetchone()
            if history:
                return history[0]
            
        # If no previous history, use neural network to generate response
        input_data = self.prepare_input(input_data)
        output_data = self.neural_network.predict(input_data)
        response = self.prepare_output(output_data)
        
        # Update context with the input and output data
        self.context = f"{input_data} {response}"
        
        return response
    
    def generate_output(self, input_text):
        # Prepare the input by tokenizing and vectorizing it
        input_vector = vectorize_input(input_text)
        
        # Generate output from the neural network
        output_vector = self.neural_network.predict(input_vector)
        output_text = vector_to_text(output_vector)
        
        # Save the input/output pair to the database
        self.database.add_entry(input_text, output_text)
        
        # Return the generated output
        return output_text
        
    def prepare_input(self, input_data):
        # Convert input data to a vector of integers
        input_vector = []
        for char in input_data:
            input_vector.append(ord(char))
        while len(input_vector) < self.input_size:
            input_vector.append(0)
        return input_vector
    
    def prepare_output(self, output_data):
        # Convert output data to a string
        output_string = ''
        for val in output_data:
            if val > 0:
                output_string += chr(round(val))
        return output_string

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_sizes, output_size):
        self.input_nodes = input_nodes
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        
        self.hidden_nodes = sum(hidden_sizes)
        
        self.weights_ih = self.randomize_weights(input_nodes, self.hidden_nodes)
        self.weights_ho = self.randomize_weights(self.hidden_nodes, output_size)
        
        self.biases_h = self.randomize_biases(self.hidden_nodes)
        self.biases_o = self.randomize_biases(output_size)

    def randomize_biases(self, size):
        return [random.uniform(-1, 1) for i in range(size)]
        
    def randomize_weights(self, n, m):
        return [[random.uniform(-1, 1) for j in range(m)] for i in range(n)]

    def predict(self, inputs):
        hidden = self.matrix_multiply(inputs, self.weights_ih)
        hidden = self.activate(hidden)
        output = self.matrix_multiply(hidden, self.weights_ho)
        output = self.activate(output)
        return output

    def activate(self, inputs):
        return [[1 / (1 + pow(2.71828, -x)) for x in row] for row in inputs]

    def matrix_multiply(self, a, b):
        result = [[0 for j in range(len(b[0]))] for i in range(len(a))]
        for i in range(len(a)):
            for j in range(len(b[0])):
                for k in range(len(b)):
                    result[i][j] += a[i][k] * b[k][j]
        return result

    def train(self, inputs, targets, iterations):
        for i in range(iterations):
            hidden = self.matrix_multiply(inputs, self.weights_ih)
            hidden = self.activate(hidden)
            output = self.matrix_multiply(hidden, self.weights_ho)
            output = self.activate(output)

            output_errors = [[targets[i][j] - output[i][j] for j in range(len(targets[0]))] for i in range(len(targets))]
            output_gradients = [[output[i][j] * (1 - output[i][j]) * output_errors[i][j] for j in range(len(targets[0]))] for i in range(len(targets))]
            hidden_errors = self.matrix_multiply(output_gradients, [[self.weights_ho[j][i] for j in range(len(self.weights_ho))] for i in range(len(self.weights_ho[0]))])
            hidden_gradients = [[hidden[i][j] * (1 - hidden[i][j]) * hidden_errors[i][j] for j in range(len(hidden[0]))] for i in range(len(hidden))]

            delta_weights_ih = self.matrix_multiply([[inputs[j][i] for j in range(len(inputs))] for i in range(len(inputs[0]))], hidden_gradients)
            delta_weights_ho = self.matrix_multiply([[hidden[j][i] for j in range(len(hidden))] for i in range(len(hidden[0]))], output_gradients)

            self.weights_ih = [[self.weights_ih[i][j] + delta_weights_ih[i][j] for j in range(len(self.weights_ih[0]))] for i in range(len(self.weights_ih))]
            self.weights_ho = [[self.weights_ho[i][j] + delta_weights_ho[i][j] for j in range(len(self.weights_ho[0]))] for i in range(len(self.weights_ho))]


if __name__ == '__main__':
    bot = ConversationBot()
    bot.load_database('conversation_history.db')
    bot.load_model('text_model.nn')
    
    print('Welcome to the ConversationBot! Type "exit" to quit.')
    while True:
        user_input = input('You: ')
        if user_input.lower() == 'exit':
            break
        
        expected_response = input('Bot: ')
        bot_output = bot.generate_output(user_input, expected_response)
        print('Bot: ' + bot_output)
        
        while True:
            satisfied = input('Was that response satisfactory? (y/n) ')
            if satisfied.lower() == 'y':
                break
            elif satisfied.lower() == 'n':
                bot.train_and_add_nodes(user_input, expected_response, num_cycles=10)
                break
            else:
                print('Invalid input. Please enter "y" or "n".')
    
    bot.save_database('conversation_history.db')
    bot.save_model('text_model.nn')
