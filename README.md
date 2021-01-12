# Homomorphically Encrypted DataFrame Query

Homomorphic encryption permits mathematical operations to be executed directly on encrypted data, yielding an encrypted result that, when decrypted, is the same as you would get on the unencrypted input.

This means that, for example, you can securely store encrypted data on a server and perform queries on it without ever having to worry about server-side encryption keys being compromised - they simply aren't there. The recipient of the data must decrypt the result.

## Simple test

```
python test_df.py
```

## Client-server demo

For the purposes of the demonstration we create a server that stores encrypted data and will aggregate it (i.e. perform addition)  on request *without requiring decryption*.

The server permits a single encrypted dataset to be uploaded (along with a corresponding public key and a encryption parameters, **but not** the private key that would permit decryption).

Then, the encrypted data can be downloaded directly, aggregrated, or deleted entirely. Only the client can actually decrypt the data.

The client script does the following:

- loads an unencrypted dataset
- encrypts the data and uploads it to the server
- asks the server for aggregated data and decrypts the result (x3)
- deletes the data from the server

First start the server:

```bash
FLASK_APP=server flask run
```

Then run the client script:

```bash
python client.py
```

You should get something like this:

```text
get before dataset has been uploaded:
400 b'no encrypted data registered'
upload encrypted dataset:
200 b'152 rows'
check dataset ok:
aggregate by area and decrypt:
                  2018     2019     2020     2021     2022
AGE GROUP SEX
0-4       F    13710.0  13474.8  13230.4  13051.3  12772.1
          M    14509.0  14111.1  13844.6  13536.2  13285.6
10-14     F    13896.0  14218.2  14570.1  14788.2  14993.0
          M    14461.0  14606.9  14940.6  15092.5  15431.4
15-19     F    12772.0  12458.8  12423.2  12861.1  13353.1
          M    13537.0  13594.8  13633.1  13933.5  14205.8
20-24     F    14168.0  13875.8  13616.7  13312.6  12859.5
          M    15684.0  15176.3  14782.1  14343.7  13970.2
25-29     F    15630.0  15629.3  15465.7  15119.7  14690.6
          M    15869.0  15933.1  15922.4  15799.0  15441.3
30-34     F    15534.0  15618.7  15588.0  15629.5  15878.5
          M    14547.0  14775.0  14942.4  15080.3  15331.5
35-39     F    14381.0  14614.9  14776.0  14955.3  15041.5
          M    13172.0  13374.1  13465.3  13589.3  13831.6
40-44     F    13038.0  13004.5  13282.7  13541.8  14038.1
          M    12306.0  12284.8  12404.8  12665.4  12956.3
45-49     F    15882.0  15443.6  14790.9  14092.4  13410.2
          M    14772.0  14269.7  13724.7  13117.1  12524.7
5-9       F    14921.0  14962.6  14898.4  14533.8  14305.5
          M    15551.0  15731.7  15619.3  15503.5  15194.0
50-54     F    17548.0  17203.3  16881.7  16586.1  16205.3
          M    16393.0  16123.8  15636.1  15253.1  14922.5
55-59     F    17069.0  17256.5  17574.7  17779.4  17627.3
          M    16232.0  16317.9  16706.6  16848.5  16609.0
60-64     F    14779.0  15314.1  15695.4  16117.8  16705.2
          M    13961.0  14321.9  14661.0  14963.9  15378.7
65-69     F    13623.0  13480.6  13453.5  13691.9  13998.4
          M    12565.0  12455.5  12493.8  12663.4  12956.3
70-74     F    12655.0  13126.8  13477.3  13504.4  12949.8
          M    11912.0  12268.8  12282.4  12348.4  11788.1
75-79     F     9132.0   9222.9   9340.3   9844.3  10748.4
          M     7893.0   8068.3   8478.4   8876.8   9758.4
80-84     F     7582.0   7773.3   7842.3   7723.6   7660.1
          M     5704.0   5946.4   5989.5   6000.4   6053.8
85-89     F     4671.0   4727.8   4816.1   4872.2   5047.5
          M     2986.0   3055.0   3137.6   3232.1   3344.0
90+       F     2784.0   2839.6   2867.8   2904.9   2924.6
          M     1242.0   1280.0   1332.8   1380.3   1432.0
aggregate by age and decrypt:
                             2018     2019     2020     2021     2022
AREA                 SEX
Darlington           F    54647.0  54721.9  54790.3  54854.8  54911.3
                     M    51919.0  51973.2  52037.8  52078.6  52112.2
Hartlepool           F    47718.0  47796.4  47863.8  47925.7  47975.2
                     M    45524.0  45569.8  45594.7  45624.0  45645.8
Middlesbrough        F    71109.0  71113.0  71063.0  71019.1  70980.7
                     M    69436.0  69418.2  69359.8  69281.6  69195.2
Redcar and Cleveland F    70301.0  70614.8  70874.1  71110.7  71341.5
                     M    66417.0  66733.9  67005.2  67243.2  67462.0
aggregate by sex and decrypt:
                                  2018    2019    2020    2021    2022
AREA                 AGE GROUP
Darlington           0-4        5917.0  5746.8  5615.3  5475.0  5410.3
                     10-14      6410.0  6508.2  6654.0  6645.2  6760.0
                     15-19      5656.0  5570.0  5601.6  5808.7  5936.3
                     20-24      5429.0  5345.8  5190.0  5019.3  4894.7
                     25-29      6267.0  6313.5  6304.3  6159.8  6026.2
...                                ...     ...     ...     ...     ...
Redcar and Cleveland 70-74      8333.0  8552.3  8598.7  8534.2  8059.4
                     75-79      5848.0  5998.0  6185.4  6517.7  7081.1
                     80-84      4228.0  4439.8  4563.6  4599.3  4656.5
                     85-89      2389.0  2461.8  2512.4  2578.1  2712.4
                     90+        1295.0  1320.8  1365.1  1394.3  1425.0

[76 rows x 5 columns]
aggregate with invalid param:
b"invalid or missing aggregation parameter: INVALID. must be one of ['AREA', 'AGE GROUP', 'SEX']"
delete encrypted data on server:
check encrypted data no longer on server:
```

## Caveats

- Each (numeric) value is encrypted individually, rather than the whole dataset. Non-numeric values are not encrypted.
- The encrypted (serialised) data is *much* larger than the original: 32MB vs 8.1kB.

## Resources

https://en.wikipedia.org/wiki/Homomorphic_encryption

https://pyfhel.readthedocs.io/en/latest/

https://blog.openmined.org/build-an-homomorphic-encryption-scclient_heme-from-scratch-with-python/
