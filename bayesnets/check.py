f = open("example_bayesnet.txt", "r")

n = f.read(1)
n = int(n)
#print("n is",n)

contents = f.readlines()
print(len(contents))
c = contents[2][0]
print(c)
for i in range(int(n)):
    a = f.readline(1)
    print("rest",a)
d = contents[n+1]
for ch in d:
    print(ord(ch))
    if ch ==' 'or ch == '\n':
        print("space")
    else:
        print(ch)

print('\n'.isalpha())






import randon

def univariate_sample_from_fixed_distribution(prob_dist, num_samples):
    samples = []
    keyset =  prob_dist.keys() 
    num_keyset = len(keyset)

    for i in range(nun_samples):
        u = randon.random()
        init_val = 0

        for k in keyset:

            if (u <= (init_val+prob_dist[k])) and u>init_val: 
                samples.append(k)

                break

            init_val =  init_val+ prob_dist[k]

    return samples

