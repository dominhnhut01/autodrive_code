import numpy as np
import skimage.graph
import  matplotlib.pyplot as plt

from skimage.morphology import skeletonize
import matplotlib.pyplot as plt
import numpy as np


directory = input('directory to image numpy file:')
image = np.load(directory)
image = np.where(image==255, 1, image)
print(np.unique(image))
skeleton = skeletonize(image)
#source = np.where(skeleton[435]==True)
size=skeleton.shape
costs = np.where(skeleton, 1, 1000)
path, cost = skimage.graph.route_through_array(
    costs, start=(5,443), end=(435,76), fully_connected=True)
result = np.zeros(size)
for i in range(len(path)) :
    result[path[i][0],path[i][1]]=1
'''
plt.imshow(image)
plt.show()
plt.imshow(skeleton)
plt.show()
plt.imshow(result)
plt.show()
'''
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(8, 4),
                         sharex=False, sharey=False)

ax = axes.ravel()

ax[0].imshow(image, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('original', fontsize=20)

ax[1].imshow(skeleton, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('skeleton', fontsize=20)

ax[2].imshow(result, cmap=plt.cm.gray)
ax[2].axis('off')
ax[2].set_title('result', fontsize=20)

fig.tight_layout()
plt.show()