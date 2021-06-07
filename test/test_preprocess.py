import logging

import pandas as pd
import pytest

import src.preprocess as preprocess

logger = logging.getLogger(__name__)


def test_clean():
    """"Happy" path unit test for clean() function

    """

    # Define input dataframe
    df_in_values = [['[\'Mamie Smith & Her Jazz Hounds\']', 0.424],
                    ['[\'Mamie Smith\']', 0.782],
                    ['[\'Mamie Smith & Her Jazz Hounds\']', 0.474],
                    ['[\'Francisco Canaro\']', 0.469],
                    ['[\'Meetya\']', 0.5710000000000001]]

    df_in_index = [5, 6, 7, 8, 9]

    df_in_columns = ['artists', 'danceability']

    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output, df_true
    df_true = pd.DataFrame(
        [['Mamie Smith & Her Jazz Hounds', 0.424],
         ['Mamie Smith', 0.782],
         ['Mamie Smith & Her Jazz Hounds', 0.474],
         ['Francisco Canaro', 0.469],
         ['Meetya', 0.5710000000000001]],
        index=[5, 6, 7, 8, 9],
        columns=['artists', 'danceability'])

    # Compute test output
    df_test = preprocess.clean(df_in)

    # Test that the true and test are the same
    assert df_test.equals(df_true)

    logger.info("Finished running test_clean()")


def test_clean_non_df():
    """"Unhappy" path unit test for clean() function

    """

    df_in = 'This is a dataframe'

    with pytest.raises(TypeError):
        preprocess.clean(df_in)

    logger.info("Finished running test_clean_non_df()")


def test_standardize():
    """"Happy" path unit test for standardize() function

    """

    # Define input dataframe
    df_in_values = [[0.991, 0.598, 0.224, 0.000522, 0.379, -12.628, 0.0936, 149.976,
                     0.634, '0cS0A1fUEUd1EW3FcF8AEI'],
                    [0.643, 0.852, 0.517, 0.0264, 0.0809, -7.261, 0.0534, 86.889,
                     0.95, '0hbkKFIJm7Z05H8Zl9w30f'],
                    [0.993, 0.647, 0.18600000000000005, 1.76e-05, 0.519, -12.098,
                     0.174, 97.6, 0.6890000000000001, '11m7laMUgmOKqI3oYzuhne'],
                    [0.000173, 0.73, 0.7979999999999999, 0.8009999999999999, 0.128,
                     -7.311, 0.0425, 127.997, 0.0422, '19Lc5SfJJ5O1oaxY0fpwfh'],
                    [0.295, 0.7040000000000001, 0.7070000000000001, 0.000246, 0.402,
                     -6.0360000000000005, 0.0768, 122.076, 0.299,
                     '2hJjbsLCytGsnAHfdsLejp'],
                    [0.996, 0.424, 0.245, 0.799, 0.235, -11.47, 0.0397, 103.87, 0.477,
                     '3HnrHGLE9u2MjHtdobfWl9'],
                    [0.992, 0.782, 0.0573, 1.61e-06, 0.17600000000000002, -12.453,
                     0.0592, 85.652, 0.487, '5DlCyqLyX2AOVDTjjkDZ8x'],
                    [0.996, 0.474, 0.239, 0.18600000000000005, 0.195, -9.712, 0.0289,
                     78.78399999999998, 0.366, '02FzJbHtqElixxCmrpSCUa'],
                    [0.996, 0.469, 0.238, 0.96, 0.149, -18.717, 0.0741, 130.06, 0.621,
                     '02i59gYdjlhBmbbWhf8YuK'],
                    [0.0068200000000000005, 0.5710000000000001, 0.753, 0.873, 0.092,
                     -6.943, 0.0446, 126.993, 0.119, '06NUxS2XL3efRh0bloxkHm']]

    df_in_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    df_in_columns = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                     'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'id']

    df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)

    # Define expected output, df_true
    df_true = pd.DataFrame(
        [[0.7376033217400042, -0.1991834703241278, -0.6705589048000257,
          -0.8910790835018826, 1.0207199420370425, -0.5932253887098508,
          0.6265442035518551, 1.7362619749286774, 0.6374868502087634,
          '0cS0A1fUEUd1EW3FcF8AEI'],
         [-0.11772942478648322, 1.6677021924924198, 0.46888179059177115,
          -0.8277460645734818, -1.1010052843853995, 0.8773028368713085,
          -0.3841731713592435, -1.073329066342884, 1.8540941981129133,
          '0hbkKFIJm7Z05H8Zl9w30f'],
         [0.7425190271798116, 0.16096376384126948, -0.8183361963525452,
          -0.8923135365024037, 2.017169226502463, -0.4480083289822537,
          2.647978953374052, -0.5963127294896545, 0.8492381291161315,
          '11m7laMUgmOKqI3oYzuhne'],
         [-1.6977035151640187, 0.7710090788561254, 1.5616559728617194,
          1.0679860809531962, -0.7657712751116759, 0.8636031142554975,
          -0.6582234048550389, 0.757423204720748, -1.640956910834515,
          '19Lc5SfJJ5O1oaxY0fpwfh'],
         [-0.9730621713129708, 0.5799105464418337, 1.20776824835437,
          -0.8917545573879727, 1.1844223244849332, 1.2129460409586794,
          0.20415485284273904, 0.49373039074371733, -0.6522709394997502,
          '2hJjbsLCytGsnAHfdsLejp'],
         [0.7498925853395226, -1.4780736487890067, -0.5888925068367912,
          1.0630913426481963, -0.004199321984533093, -0.2759398129276667,
          -0.728621629973225, -0.31707713691475453, 0.03303319950954951,
          '3HnrHGLE9u2MjHtdobfWl9'],
         [0.7400611744599078, 1.1532061436847103, -1.3188345495843687,
          -0.8923526699351523, -0.42413152043781727, -0.5452763595545118,
          -0.23834827647157258, -1.1284190867599733, 0.0715334320381619,
          '5DlCyqLyX2AOVDTjjkDZ8x'],
         [0.7498925853395226, -1.110576471069214, -0.6122257633977153,
          -0.4371459478344449, -0.28889911754608166, 0.20574243424425043,
          -1.000157641143371, -1.4342867183077272, -0.39431938155804747,
          '02FzJbHtqElixxCmrpSCUa'],
         [0.7498925853395226, -1.1473261888411934, -0.6161146394912027,
          1.4571177762007328, -0.6163038824418628, -2.2615776088633215,
          0.1362708500502027, 0.8492992856588689, 0.5874365479215673,
          '02i59gYdjlhBmbbWhf8YuK'],
         [-1.6813661681348187, -0.3976319462928153, 1.3866565486547884,
          1.244196659933213, -1.0220010911170698, 0.9644330727078669,
          -0.6054247360163995, 0.7127098817629808, -1.3452751250147723,
          '06NUxS2XL3efRh0bloxkHm']],
        index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        columns=['acousticness', 'danceability', 'energy', 'instrumentalness',
                 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'id']
    )

    # Compute test output
    df_test = preprocess.standardize(df_in)

    # Test that the true and test are the same
    assert df_test.equals(df_true)

    logger.info("Finished running test_standardize()")


def test_standardize_non_df():
    """"Unhappy" path unit test for standardize() function

    """

    df_in = 'This is a dataframe'

    with pytest.raises(TypeError):
        preprocess.standardize(df_in)

    logger.info("Finished running test_standardize_non_df()")


def run_tests():
    """Calls other functions to run the tests

    """
    logger.info("Start running tests")

    test_clean()
    test_clean_non_df()
    test_standardize()
    test_standardize_non_df()

    logger.info("Finish running all tests")
