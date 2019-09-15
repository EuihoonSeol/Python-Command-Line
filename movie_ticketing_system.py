import json


def get_movies(file_name):
    with open(file_name) as f:
        data = json.load(f)
        return data


def get_movies_genres(movies):
    genre_list = []
    for genre in movies:
        genre_list.append(genre)
    return genre_list


def get_movies_titles(movies):
    title_list = []
    for genre in movies:
        for movie in movies[genre]:
            title_list.append(movie['title'])
    return title_list


class App:

    welcome_page = '''Hello, welcome to Movie Ticketing System\n
    1. List all available movies.
    2. Show my movies.
    3. Purchase a movie.
    4. Show credit balance.
    5. Exit\n'''
    genre_page = '''\nThe following is a list of movie genres\n'''
    movie_name_input_request = 'Please enter the name of movie you wish to purchase: '
    movie_number_input_request = 'Please enter the number of movie you wish to purchase: '
    number_input_request = 'Please enter number: '
    thank_you_message = 'Thank you for using our services!'
    available_movies = get_movies('available_movies.json')
    available_movies_genres = get_movies_genres(available_movies)
    available_movies_titles = get_movies_titles(available_movies)

    def __init__(self):
        self.my_movies = get_movies('my_movies.json')
        self.my_movies_genres = get_movies_genres(self.my_movies)
        self.my_movies_titles = get_movies_titles(self.my_movies)

    def load_welcome_page(self):
        while True:
            print('----------------------------------------------------')
            print(App.welcome_page)
            try:
                user_input = input(App.number_input_request)
                val = int(user_input)
                if val not in [1, 2, 3, 4, 5]:
                    print("That's not an integer between 1 to 5 !")
                elif val == 1:
                    self.load_available_movies_page()
                elif val == 2:
                    self.load_my_movies_page()
                elif val == 3:
                    self.load_purchase_movie_page()
                elif val == 4:
                    self.load_credit_balance_page()
                else:
                    print(App.thank_you_message)
                    break
            except ValueError:
                print("That's not an integer between 1 to 5 !")

    def load_available_movies_page(self):
        while True:
            print('----------------------------------------------------')
            print(App.genre_page)
            print('    0. Go back to main menu')
            for i in range(len(App.available_movies_genres)):
                print('    ' + str(i + 1) + '. ' + App.available_movies_genres[i])
            print('')
            try:
                user_input = input(App.number_input_request)
                val = int(user_input)
                if val not in range(len(App.available_movies_genres) + 1):
                    print("That's not an integer between 0 to " + str(len(App.available_movies_genres)) + " !")
                elif val == 0:
                    break
                else:
                    print('Genre: ' + App.available_movies_genres[val - 1] + '\n')
                    for i in App.available_movies[App.available_movies_genres[val - 1]]:
                        print('title: ' + i['title'] + ',')
                        print('rating: ' + str(i['rating']) + ',')
                        print('cost: ' + str(i['cost']) + '\n')
            except ValueError:
                print("That's not an integer between 0 to " + str(len(App.available_movies_genres)) + " !")

    def load_my_movies_page(self):
        for genre in self.my_movies_genres:
            print('Genre: ' + genre + '\n')
            for movie in self.my_movies[genre]:
                print('title: ' + movie['title'] + ',')
                print('rating: ' + str(movie['rating']) + ',')
                print('watched: ' + str(movie['watched']) + '\n')

    def load_credit_balance_page(self):
        print('----------------------------------------------------')
        print('    Your current credit balance : ' + str(self.credit_balance))

    def load_purchase_movie_page(self):
        while True:
            print('----------------------------------------------------')
            try:
                user_input = input(App.movie_name_input_request)
                val = str(user_input)
                if len(val) < 3:
                    print("You must type at least three characters for the search to be valid.")
                elif val not in App.available_movies_titles:
                    print("No movies found matching " + val)
                    break
                else:
                    search_results = []
                    for title in App.available_movies_titles:
                        if val in title:
                            search_results.append(val)
                    while True:
                        try:
                            print("The following is a list of possible matches")
                            for index, value in enumerate(search_results):
                                print(str(index) + " : " + str(value))
                            user_input = input(App.movie_number_input_request)
                            val = int(user_input)
                            if val not in range(len(search_results)):
                                print("That's not an integer between 0 to " + str(len(search_results) - 1) + " !")
                            else:
                                title = search_results[int(val)]
                                break
                        except ValueError:
                            print("That's not an integer between 0 to " + str(len(search_results) - 1) + " !")

                    if title not in self.my_movies_titles:
                        genre_movie = App.get_movie_by_title(title)
                        if self.credit_balance < genre_movie[list(genre_movie.keys())[0]]['cost']:
                            print("Not enough credit remaining to purchase this movie.")
                        else:
                            self.credit_balance = self.credit_balance - genre_movie[list(genre_movie.keys())[0]]['cost']
                            print("Your current credit is " + str(self.credit_balance) + " = " + str(self.credit_balance + genre_movie[list(genre_movie.keys())[0]]['cost']) + " - " + str(genre_movie[list(genre_movie.keys())[0]]['cost']))

                            with open('my_movies.json', 'r+') as f:
                                data = json.load(f)
                                if list(genre_movie.keys())[0] in self.my_movies_genres:
                                    data[list(genre_movie.keys())[0]].append(genre_movie[list(genre_movie.keys())[0]])
                                else:
                                    self.my_movies_genres.append(list(genre_movie.keys())[0])
                                    genre_movie_list = []
                                    genre_movie_list.append(genre_movie[list(genre_movie.keys())[0]])
                                    data[list(genre_movie.keys())[0]] = genre_movie_list
                                f.seek(0)
                                f.write(json.dumps(data))
                                f.truncate()
                                self.my_movies = data
                                self.my_movies_titles.append(genre_movie[list(genre_movie.keys())[0]]['title'])
                                break
                    else:
                        print("You have already purchased this movie.")
                        break
            except ValueError:
                print("An value exception occurred")

    def get_movie_by_title(title):
        genre_movie = {}
        for genre in App.available_movies:
            for movie in App.available_movies[genre]:
                if title == movie['title']:
                    movie['watched'] = False
                    genre_movie[genre] = movie
                else:
                    pass
        return genre_movie



class User(App):

    def __init__(self):
        App.__init__(self)
        self.credit_balance = 100



user = User()
user.load_welcome_page()