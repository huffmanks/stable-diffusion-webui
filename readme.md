## Create venv

```sh
python3 -m venv venv
```

## Activate venv

```sh
source venv/bin/activate
```

## Install deps

```sh
pip install -r requirements.txt
```

## Models

- [CyberRealistic Pony Catalyst V30](https://civitai.com/models/1502316/cyberrealistic-pony-catalyst)
- [Deliberate Cyber v5](https://civitai.com/models/357827/deliberate-cyber)

## Embeddings

[CyberRealistic Pony - Negative - v2](https://civitai.com/models/77976/cyberrealistic-negative-pony-v20)

## ESRGAN

- [4x-UltraSharp.pth](https://huggingface.co/lokCX/4x-Ultrasharp/tree/main)
- [Real-ESRGAN_x4.pth](https://huggingface.co/ai-forever/Real-ESRGAN/tree/main)

## VAE

[vae-ft-mse-840000-ema-pruned](https://huggingface.co/EvilEngine/vae-ft-mse-840000-ema-pruned/blob/main/vae-ft-mse-840000-ema-pruned.safetensors)

## ControlNet

1. Open "Extensions" tab.
2. Open "Install from URL" tab in the tab.
3. Enter https://github.com/Mikubill/sd-webui-controlnet.git to "URL for extension's git repository".
4. Press "Install" button.
5. Wait for 5 seconds, and you will see the message "Installed into stable-diffusion-webui\extensions\sd-webui-controlnet. Use Installed tab to restart".
6. Go to "Installed" tab, click "Check for updates", and then click "Apply and restart UI". (The next time you can also use these buttons to update 7. ControlNet.)
7. Completely restart A1111 webui including your terminal. (If you do not know what is a "terminal", you can reboot your computer to achieve the same 9. effect.)
8. [Download models](https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/tree/main)
   - control_canny-fp16.safetensors
   - control_depth-fp16.safetensors
   - control_openpose-fp16.safetensors
   - control_lineart_lora.safetensors
   - control_mlsd_lora.safetensors
