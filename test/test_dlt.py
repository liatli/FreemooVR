#!/usr/bin/env python
import numpy as np

# ROS imports
import roslib; roslib.load_manifest('flyvr')
import dlt
import camera_model

# some sample data -----------------------

XYZ = np.array([[  2.00000000e-02,   0.00000000e+00,   0.00000000e+00],
                [  1.22464680e-18,   0.00000000e+00,   2.00000000e-02],
                [  1.41421356e-02,   0.00000000e+00,  -1.41421356e-02],
                [  1.41421356e-02,   0.00000000e+00,   1.41421356e-02],
                [ -3.67394040e-18,  -2.00000000e-02,   0.00000000e+00],
                [  1.22464680e-18,   2.00000000e-02,   0.00000000e+00],
                [  1.00000000e-02,   1.00000000e-02,  -1.41421356e-02],
                [  1.00000000e-02,  -1.00000000e-02,  -1.41421356e-02],
                [  1.41421356e-02,   1.41421356e-02,   0.00000000e+00],
                [  1.41421356e-02,  -1.41421356e-02,   0.00000000e+00],
                [  2.00000000e-02,   0.00000000e+00,   0.00000000e+00],
                [  1.22464680e-18,   0.00000000e+00,   2.00000000e-02],
                [  1.41421356e-02,   0.00000000e+00,  -1.41421356e-02],
                [  1.41421356e-02,   0.00000000e+00,   1.41421356e-02],
                [ -3.67394040e-18,  -2.00000000e-02,   0.00000000e+00],
                [  1.22464680e-18,   2.00000000e-02,   0.00000000e+00],
                [  1.00000000e-02,   1.00000000e-02,  -1.41421356e-02],
                [  1.00000000e-02,  -1.00000000e-02,  -1.41421356e-02],
                [  1.41421356e-02,   1.41421356e-02,   0.00000000e+00],
                [  1.41421356e-02,  -1.41421356e-02,   0.00000000e+00]])

xy = np.array([[ 467.85551727,  663.68835971],
               [ 466.81674246,  590.70322096],
               [ 469.81695678,  723.93789261],
               [ 469.3536242 ,  616.7838872 ],
               [ 389.60089819,  678.51156788],
               [ 549.99472131,  667.72203292],
               [ 522.4649629 ,  725.09611373],
               [ 415.840405  ,  729.02607287],
               [ 524.74859392,  665.29342667],
               [ 414.28125927,  665.94255981],
               [ 467.85551727,  663.68835971],
               [ 466.81674246,  590.70322096],
               [ 469.81695678,  723.93789261],
               [ 469.3536242 ,  616.7838872 ],
               [ 389.60089819,  678.51156788],
               [ 549.99472131,  667.72203292],
               [ 522.4649629 ,  725.09611373],
               [ 415.840405  ,  729.02607287],
               [ 524.74859392,  665.29342667],
               [ 414.28125927,  665.94255981]])


# the tests -------------------
def test_basic_dlt():
    results = dlt.dlt(XYZ, xy, ransac=False)
    print results['mean_reprojection_error']
    assert results['mean_reprojection_error'] < 6.0

    results2 = dlt.dlt(XYZ, xy, ransac=False, flip=True)
    print results2['mean_reprojection_error']
    assert results2['mean_reprojection_error'] < 6.0

    #assert not np.allclose(results['pmat'], results2['pmat'])

    c1 = camera_model.load_camera_from_pmat(  results['pmat']  )
    c2 = camera_model.load_camera_from_pmat( results2['pmat'] )
    print 'c1.get_lookat(), c2.get_lookat()',c1.get_lookat(), c2.get_lookat()
    assert not np.allclose( c1.get_lookat(), c2.get_lookat() )
    assert not np.allclose(results['pmat'], results2['pmat'])

def xtest_ransac_dlt():
    np.random.seed(3) # try to prevent following from failing occasionally
    results = dlt.dlt(XYZ, xy, ransac=True)
    assert results['mean_reprojection_error'] < 5.0

    results2 = dlt.dlt(XYZ, xy, ransac=True, flip=True)
    assert results2['mean_reprojection_error'] < 5.0
