from defaults import SineTone, two_octaves_symm, a3
from chord_plots import roughness_curve
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

# Dissertation ch. 2, figure 1
# Figure 1a. A plot of Helmholtz’s pair-roughness function (Helmholtz 1895, appendix XV)
def ch2_fig1a(action):
    title = 'ch2_fig1a'

    ref_tone = SineTone(a3)
    test_tone = SineTone(a3)
    T = two_octaves_symm

    roughness = roughness_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='HELMHOLTZ',
        normalize=True,
        options={
            'crossterms_only': False,
            'ref': ref_tone.partials['hz'],
            'show_partials': False
        }
    )

    # Plot
    _, ax = plt.subplots()
    plt.plot(T.domain, roughness, 'k')
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    plt.subplots_adjust(left=0.15)
    ax.yaxis.set_label_coords(-0.13, 0.5)

    if action.lower() == 'save':
        plt.savefig(f'{title}.png',dpi=350)
        print(f'{title}.png saved')

    else:
        plt.show()
