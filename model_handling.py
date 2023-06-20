from cheetahpyanalytics import metric_functions


class pmc:
    def __init__(self, load_data, load_metric, ctl_days, atl_days):
        self.load_data = load_data
        self.load_metric = load_metric
        self.ctl_param = 1/ctl_days
        self.atl_param = 1/atl_days
    
    def calculate_ewma(self, load:np.array, k:float):
        current = (1-k) * Yesterday’s CTL + k * Today’s TSS

    def strided_app(a, L, S): # Window len = L, Stride len/stepsize = S
        nrows = ((a.size - L) // S) + 1
        n = a.strides[0]
        return np.lib.stride_tricks.as_strided(a, shape=(nrows, L), strides=(S * n, n))

    def numpyEWMA(price, windowSize):
        weights = np.exp(np.linspace(-1., 0., windowSize))
        weights /= weights.sum()

        a2D = strided_app(price, windowSize, 1)

        returnArray = np.empty((price.shape[0]))
        returnArray.fill(np.nan)
        for index in (range(a2D.shape[0])):
            returnArray[index + windowSize-1] = np.convolve(weights, a2D[index])[windowSize - 1:-windowSize + 1]
        return np.reshape(returnArray, (-1, 1))

class performance_model():