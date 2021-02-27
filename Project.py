import random
from tkinter import *
from tkinter import messagebox
from Words import word_list
from PIL import Image, ImageTk

root = Tk()
root.geometry('800x500+300+100')
root.configure(bg='white')
root.iconbitmap('D:/Facultate/Curs Python Google/pythonProject/Hangman Icon.ico')
root.title('Hangman')

global start_button, quit_button, input_textbox
global letter_list, word, number_of_lives


def resize_image(image_name, width, height):
    image = Image.open(image_name + '.jpg')
    image = image.resize((width, height), Image.ANTIALIAS)
    returned_image = ImageTk.PhotoImage(image)
    return returned_image


logo = resize_image('Hangman', 110, 130)
image_label = Label(root, image=logo, bd=0, width=110, height=130)
image_label.place(x=340, y=100)


word_label = Label(root, text='', font=('arial', 27, 'bold'), bg='white', anchor=CENTER)
word_label.place(x=300, y=180)

answer_label = Label(root, text='', font=('arial', 25, 'bold'), bg='white', anchor=CENTER)
answer_label.place(x=100, y=450)

lives_left = Label(root, text='', font=('arial', 25, 'bold'), bg='white')
lives_left.place(x=580, y=100)


def start():
    global root, start_button, quit_button, lives_left
    title = Label(root, text='Hangman Game', font=('arial', 35, 'bold'), bg='white')
    title.place(x=225, y=25)
    lives_left = Label(root, text='', font=('arial', 25, 'bold'), bg='white')
    lives_left.place(x=580, y=100)
    start_button = Button(root, text='Start Game', font=('arial', 15, 'bold'), width=15, bd=5, bg='red',
                          activebackground='gray65', activeforeground='black', command=game_page)
    start_button.place(x=300, y=270)
    quit_button = Button(root, text='Quit Game', font=('arial', 15, 'bold'), width=15, bd=5, bg='red',
                         activebackground='gray65', activeforeground='black', command=root.destroy)
    quit_button.place(x=300, y=350)


def game_page():
    global root, start_button, quit_button, letter_list, word, number_of_lives
    number_of_lives = 7
    start_button.place_forget()
    quit_button.place_forget()
    image_label.place_forget()
    lives_left.configure(text=f'Lives Left = {number_of_lives}')
    word = get_random_word()
    print(word)
    letter_list = display_underline()
    get_input()


def get_random_word():
    return random.choice(word_list)


def display_underline():
    global letter_list, word
    letter_list = ["_" for _ in word]
    if len(word) >= 6:
        letter_list[0] = word[0]
        letter_list[len(word) - 1] = word[len(word) - 1]
    hidden_word = ''
    for i in letter_list:
        hidden_word += i + '  '
    word_label.configure(text=hidden_word, anchor=CENTER)
    answer_label.configure(text='')
    return letter_list


def get_input():
    global root, input_textbox
    input_text = StringVar(root)
    input_textbox = Entry(root, font=('arial', 25, 'bold'), relief=RIDGE, bd=5, bg='gray65', justify='center',
                          fg='white',
                          textvariable=input_text)
    input_textbox.focus_set()
    input_textbox.place(x=210, y=250)
    submit_button = Button(root, text='Submit', font=('arial', 15, 'bold'), width=15, bd=5, bg='red',
                           activebackground='white', activeforeground='black',
                           command=lambda: verify_letter(input_text.get()))
    submit_button.place(x=300, y=350)


def verify_letter(character):
    global letter_list, word, number_of_lives, image_label
    if not character.isalpha():
        messagebox.showerror("Notification", 'You have not entered a letter!')
        input_textbox.delete(0, 'end')
        return
    if character.isupper():
        messagebox.showerror("Notification", 'You have not entered a lowercase letter!')
        input_textbox.delete(0, 'end')
        return
    if len(character) > 1:
        if character == word:
            result = messagebox.askyesno("Notification", f'You guessed the word! \nDo you want to play again?')
            if result:
                game_page()
        else:
            messagebox.showerror("Notification", 'You have entered more than a letter!')
            input_textbox.delete(0, 'end')
            return
    letter_guessed = 0
    input_textbox.delete(0, 'end')
    if number_of_lives > 1:
        for i in range(len(letter_list)):
            if character == word[i]:
                letter_list.pop(i)
                letter_list.insert(i, character)
                word_label.configure(text=letter_list)
                letter_guessed = 1
        if letter_guessed == 0:
            number_of_lives -= 1
            lives_left.configure(text=f'Lives Left = {number_of_lives}')
        if "_" not in letter_list:
            result = messagebox.askyesno("Notification", f'You guessed the word! \nDo you want to play again?')
            if result:
                game_page()
            else:
                root.destroy()
    else:
        number_of_lives -= 1
        lives_left.configure(text=f'Lives Left = {number_of_lives}')
        result = messagebox.askyesno("Notification", f'You lost! The word was {word} \nDo you want to play again?')
        if result:
            game_page()
        else:
            root.destroy()


def main():
    global root
    start()
    root.mainloop()


if __name__ == "__main__":
    main()
