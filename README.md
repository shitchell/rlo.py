# rlo.py
a simple library and command line utility for reversing text using the RLO 
character

## usage

*the text provided should include {brackets} around the word(s) to be reversed*

### as a library

```py
>>> import rlo
>>> rlo.insert_markers("a simple library and {command line} utility")
'a simple library and \u202ecommand line\u202c utility'
>>> print("hello " + rlo.RLO + "world")
hello ‮world
```

### on the command line

```shell
$ python3 rlo.py a simple library and {command line} utility
a simple library and ‮command line‬ utility
$ echo "it also {accepts} piped input" | python3 rlo.py
it also ‮accepts‬ piped input
```

### caveat

the RLO character will not display properly on most devices when it appears at 
the beginning of a line, e.g.
```py
>>> print(rlo.insert_markers("this {will be reversed}"))
this ‮will be reversed‬
>>> print(rlo.insert_markers("{this will not be reversed}"))
this will not be reversed‬
```

a zero-width character placed before it will not help. to ensure that your text
appears reversed on all devices, you must have *some* visible character before
the RLO character.

## how it works

this utility makes use of the Right to Left Override (LRO) unicode character 
`U+202E`, which forces text to be displayed right-to-left. when placed before
some text, all of the text that follows will be reversed:

`let's reverse \u202Esome text` -> let's reverse ‮some text asdf

we can reverse only a certain subsection of the text by adding a stopping
character `U+202C` that marks where the text should stop displaying 
right-to-left:

`let's \u202Ereverse\u202C some text` -> let's ‮reverse‬ some text

## why this is important

this trick can be used to bypass text filters and make malicious urls look real.

### malicious urls

if an attacker wants you to visit a malicious site, they can:

1. append the reversed version of a legitimate url to their malicious url
2. reverse the entire url

when reversed, the legitimate domain will *appear* in front and as if the user
is clicking on a safe, trusted domain. example:

i want you to visit [https://malicious.com/virus.exe](#). i can manually reverse
(without the RLO character) the characters in [google.com/](#) which gives me:
*/moc.elgoog*. next i'll append this reversed domain on the end of my malicious
url:
[https://malicious.com/virus.exe#/moc.elgoog](#)

web browsers will ignore anything after a `#`, so adding this doesn't affect
my malicious url. lastly, i'll reverse everything in the brackets:

[https://{malicious.com/virus.exe#/moc.elgoog}](#) -> 
[https://‮malicious.com/virus.exe#/moc.elgoog‬](#)

if i shorten my malicious url using a service like bit.ly, it looks even more
legitimate:

[https://{bit.ly/8s2Kjf3#/moc.elgoog}](#) -> 
[https://‮bit.ly/8s2Kjf3#/moc.elgoog‬](#)

### bypassing text filters

by reversing a banned word and adding an RLO character. the actual text will be
skipped by the filter because it'll just be random letters. but when displayed,
the reversed letters will appear as the banned text.  
e.g. if the word "puppies" were banned:

`here are my \u202Eseippup\u202C` -> here are my ‮seippup‬

the user types the reverse of the banned word, `seippup`, which will not be
filtered because it's not even a word. but when the RLO character is added, it
gets displayed like a normal word

### fighting the good fight

always be sure to double check the url before entering your credentials into
a website. even if the link you clicked *looked* legitimate, there are more ways
than this to falsify links. for admins in charge of text filters, you can safely
filter the RLO character `U+202E`. it's an *override* character. legitimate text
in a language read right-to-left will use either the Right to Left Isolate
`U+2067` or Right to Left Embedding `U+202B` characters.

## reference

https://www.w3.org/International/questions/qa-bidi-unicode-controls
