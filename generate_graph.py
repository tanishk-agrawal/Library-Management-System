import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def genarate_pie(n):
    label, value=[], []
    for item in n:
        if n[item] >0:
            label.append(f'{item}({n[item]})')
            value.append(n[item])
    
    plt.clf()
    plt.pie(value, labels = label, labeldistance=1, radius=1.25, wedgeprops=dict(width=0.7, edgecolor='w'))
    plt.title('Distribution of Books in Sections', pad=15, color='#333333', weight='bold')
    plt.savefig("static/stats/section_piechart.png")

def generate_rating_pareto(b_rating):
    rating=[]
    for item in b_rating:
        rating.append((b_rating[item],item))
    rating.sort(reverse=True)

    label, value=[],[]
    for (l,v) in rating:
        label.append(l)
        value.append(v)

    plt.clf()
    plt.bar(value, label, edgecolor='black')
    plt.ylabel('Average Rating', labelpad=15, color='#333333')
    plt.ylim(top = 5.5)
    plt.title('Average Rating of Books in Sections', pad=15, color='#333333', weight='bold')
    plt.savefig("static/stats/rating_pareto.png")